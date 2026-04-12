import pandas as pd
from scipy.stats import randint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV 
from sklearn import metrics 
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import  DecisionTreeRegressor
from scipy.optimize import curve_fit
from sklearn.svm import SVC


files = [
    r"adatbazisok\adatok2022.csv",
    r"adatbazisok\adatok2023.csv",
    r"adatbazisok\adatok2024.csv"
]

dfs = []

#3 év beolvasása
for f in files:
    df = pd.read_csv(f, sep=";", encoding="utf-8-sig")
    df["ev"] = f[-8:-4]  # év kiemelése a fájlnévből (2022, 2023, 2024)
    dfs.append(df)

#Szűrés
data = pd.concat(dfs, ignore_index=True)
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
megye_col = data["Megye"].astype(str)
for col in data.columns:
    if col != "Megye":
        data[col] = (
            data[col]
            .astype(str)
            .str.replace(r'\s+', '', regex=True)
            .str.replace(',', '.')
        )
        data[col] = pd.to_numeric(data[col], errors='coerce')
data["Megye"] = megye_col

#Per capita
data['Autó/fő'] = data['auto allomany'] / data['Nepesseg']
data['Új/fő'] = data['uj auto'] / data['Nepesseg']
data['Használt/fő'] = data['hasznalt'] / data['Nepesseg']

#Megye rangsor
kereset_rang = (
    data.groupby("Megye")["atlag kereset"]
    .mean()
    .sort_values()
    .reset_index()
)

kereset_rang["Vármegye"] = kereset_rang["atlag kereset"].rank(method="dense").astype(int)

data = data.merge(kereset_rang[["Megye", "Vármegye"]], on="Megye", how="left")


numeric_columns = data.select_dtypes(include=['int', 'float']).columns.tolist()

if "Vármegye" not in numeric_columns:
    numeric_columns.append("Vármegye")

new_data = data[numeric_columns]

label_map = {
    "Nepesseg": "Népesség",
    "atlag kereset": "Átlagkereset",
    "auto allomany": "Autóállomány",
    "uj auto": "Új",
    "hasznalt": "Használt",
    "eletkor": "Átlag életkor",
    "ev": "Év",
    "Autó/fő": "Autó / fő",
    "Új/fő": "Új / fő",
    "Használt/fő": "Használt / fő",
    "Vármegye": "Vármegye"
}

#KORRELÁCIÓ
corr_matrix = new_data.corr()
corr_matrix_renamed = corr_matrix.rename(index=label_map, columns=label_map)

#HEATMAP
fig, ax = plt.subplots(figsize=(12, 9))

sns.heatmap(
    corr_matrix_renamed,
    annot=True,
    cmap='viridis',
    linewidths=0.5,
    annot_kws={"size": 8},
    ax=ax
)
plt.title('Korrelációs heatmap', fontsize=16, pad=5)
pos = ax.get_position()
ax.set_position([pos.x0, pos.y0 + 0.07, pos.width, pos.height])

plt.show()








#MODELL
df_rev = data[['atlag kereset', 'eletkor']].dropna()

X = df_rev[['atlag kereset']]
y = df_rev['eletkor']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


data['age_class'] = (data['eletkor'] > data['eletkor'].median()).astype(int)

X = new_data.drop('eletkor', axis=1)
y = data['age_class']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#DÖNTÉSI FA OSZTÁLYOZÓ
dt_clf = DecisionTreeClassifier(random_state=42)
dt_clf.fit(X_train, y_train)

dt_pred = dt_clf.predict(X_test)

print("=== Decision Tree Classifier ===")
print("Accuracy:", metrics.accuracy_score(y_test, dt_pred))
print(metrics.classification_report(y_test, dt_pred))

cm_dt = confusion_matrix(y_test, dt_pred)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix – Decision Tree")
plt.xlabel("Jósolt")
plt.ylabel("Valós")
plt.show()


#RANDOM FOREST OSZTÁLYOZÓ
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)

rf_pred = rf_clf.predict(X_test)

print("=== Random Forest Classifier ===")
print("Accuracy:", metrics.accuracy_score(y_test, rf_pred))
print(metrics.classification_report(y_test, rf_pred))

cm_rf = confusion_matrix(y_test, rf_pred)
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens')
plt.title("Confusion Matrix – Random Forest")
plt.xlabel("Jósolt")
plt.ylabel("Valós")
plt.show()




log_clf = LogisticRegression(max_iter=500)
log_clf.fit(X_train, y_train)

log_pred = log_clf.predict(X_test)

print("=== Logistic Regression ===")
print("Accuracy:", metrics.accuracy_score(y_test, log_pred))
print(metrics.classification_report(y_test, log_pred))

cm_log = confusion_matrix(y_test, log_pred)
sns.heatmap(cm_log, annot=True, fmt='d', cmap='Oranges')
plt.title("Confusion Matrix – Logistic Regression")
plt.xlabel("Jósolt")
plt.ylabel("Valós")
plt.show()


#REGRESSZIÓ
df_exp = data[['eletkor', 'atlag kereset']].dropna().copy()

df_exp = df_exp.sort_values(by='eletkor')

x_data = df_exp['eletkor'].values
y_data = df_exp['atlag kereset'].values

x0 = x_data.mean()
def exp_model(x, a, b, c):
    return a * np.exp(b * (x - x0)) + c

a0 = y_data.max() - y_data.min()
b0 = -0.15
c0 = y_data.min()

params, _ = curve_fit(
    exp_model,
    x_data,
    y_data,
    p0=[a0, b0, c0],
    maxfev=20000
)

a, b, c = params
x_curve = np.linspace(x_data.min(), x_data.max(), 400)
y_curve = exp_model(x_curve, a, b, c)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df_exp['eletkor'], y=df_exp['atlag kereset'], alpha=0.6)
plt.plot(x_curve, y_curve, color='red', linewidth=2.5, label='Exponenciális regresszió')

plt.xlabel("Autók átlagéletkora")
plt.ylabel("Átlagkereset")
plt.title("Exponenciális regresszió: életkor vs kereset")
plt.legend()
plt.show()

y_pred = exp_model(x_data, a, b, c)
r2 = r2_score(y_data, y_pred)
rmse = np.sqrt(mean_squared_error(y_data, y_pred))

print("Exponenciális modell paraméterei:")
print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"Modell: y = {a:.4f} * exp({b:.4f} * (x - {x0:.4f})) + {c:.4f}")
print(f"R^2 = {r2:.4f}")
print(f"RMSE = {rmse:.4f}")
