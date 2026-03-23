import pandas as pd
from scipy.stats import randint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV 
from sklearn import metrics 
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score

# --- Fájlok (2022 is bekerült) ---
files = [
    r"adatbazisok\adatok2022.csv",
    r"adatbazisok\adatok2023.csv",
    r"adatbazisok\adatok2024.csv"
]

dfs = []

# --- Mindhárom év beolvasása (BOM eltávolítással) ---
for f in files:
    df = pd.read_csv(f, sep=";", encoding="utf-8-sig")
    df["ev"] = f[-8:-4]  # év kiemelése a fájlnévből (2022, 2023, 2024)
    dfs.append(df)

# --- Összefűzés ---
data = pd.concat(dfs, ignore_index=True)

# --- Unnamed oszlopok törlése ---
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# --- Megye oszlop külön kezelése ---
megye_col = data["Megye"].astype(str)

# --- Tisztítás: whitespace eltávolítása minden más oszlopból ---
for col in data.columns:
    if col != "Megye":
        data[col] = (
            data[col]
            .astype(str)
            .str.replace(r'\s+', '', regex=True)
            .str.replace(',', '.')
        )
        data[col] = pd.to_numeric(data[col], errors='coerce')

# --- Megye visszaállítása ---
data["Megye"] = megye_col

# --- Per capita mutatók ---
data['Autó/fő'] = data['auto allomany'] / data['Nepesseg']
data['Új/fő'] = data['uj auto'] / data['Nepesseg']
data['Használt/fő'] = data['hasznalt'] / data['Nepesseg']

# --- Megyék rangsorolása átlagkereset alapján ---
kereset_rang = (
    data.groupby("Megye")["atlag kereset"]
    .mean()
    .sort_values()
    .reset_index()
)

kereset_rang["Vármegye"] = kereset_rang["atlag kereset"].rank(method="dense").astype(int)

# --- Visszacsatolás ---
data = data.merge(kereset_rang[["Megye", "Vármegye"]], on="Megye", how="left")

# --- Csak numerikus oszlopok kiválasztása ---
numeric_columns = data.select_dtypes(include=['int', 'float']).columns.tolist()

if "Vármegye" not in numeric_columns:
    numeric_columns.append("Vármegye")

new_data = data[numeric_columns]

# --- Szép magyar feliratok ---
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

# --- Korreláció ---
corr_matrix = new_data.corr()
corr_matrix_renamed = corr_matrix.rename(index=label_map, columns=label_map)

# --- Heatmap ---
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






""" data['target'] = (data['atlag kereset'] > data['atlag kereset'].median()).astype(int)
# --- Feature-ök és target ---
X = new_data.drop('atlag kereset', axis=1)  # vagy 'target', ha azt használod
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Jósolt')
plt.ylabel('Valós')
plt.title('Confusion Matrix')
plt.show()

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

print(metrics.classification_report(y_test, y_pred))

y = new_data['atlag kereset']

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
print(metrics.classification_report(y_test, y_pred)) """


# ================================
# REGRESSZIÓ: átlagkereset jóslása
# ================================

# --- Feature-ök (csak relevánsak) ---
X = data[['eletkor', 'Autó/fő', 'Új/fő', 'Használt/fő']]

# --- Target ---
y = data['atlag kereset']

data_clean = data[['atlag kereset', 'eletkor', 'Autó/fő', 'Új/fő', 'Használt/fő']].dropna()

X = data_clean[['eletkor', 'Autó/fő', 'Új/fő', 'Használt/fő']]
y = data_clean['atlag kereset']

# --- Train-test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Modell ---
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# --- Jóslás ---
y_pred = model.predict(X_test)

# --- Kiértékelés ---
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

plt.figure(figsize=(8,6))
sns.scatterplot(x=data['eletkor'], y=data['atlag kereset'])
plt.xlabel("Autók átlagéletkora")
plt.ylabel("Átlagkereset")
plt.title("Kapcsolat: életkor vs kereset")
plt.show()