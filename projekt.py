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

data = pd.read_csv(
    r"adatbazisok\adatok2024.csv",
    sep=";",
    encoding="cp1250",
    header=0
)

# --- Felesleges Unnamed oszlopok törlése ---
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# --- Minden oszlop tisztítása és konvertálása ---
for col in data.columns:
    data[col] = (
        data[col]
        .astype(str)
        .str.replace(' ', '')
        .str.replace(',', '.')
    )
    data[col] = pd.to_numeric(data[col], errors='coerce')

# --- Eredeti adatok ellenőrzése ---
print(data[['Nepesseg', 'auto allomany', 'uj auto', 'hasznalt']].head(10))

# --- Csak numerikus oszlopok kiválasztása ---
numeric_columns = data.select_dtypes(include=['int', 'float'])
new_data = data[numeric_columns.columns]

# --- Korrelációs mátrix ---
corr_matrix = new_data.corr()

# --- Heatmap ---
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap (Per Capita Mutatókkal)')
plt.show()



