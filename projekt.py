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


# --- Fájlok ---
files = [
    r"adatbazisok\adatok2023.csv",
    r"adatbazisok\adatok2024.csv"
]

dfs = []

# --- Mindkét év beolvasása (BOM eltávolítással) ---
for f in files:
    df = pd.read_csv(f, sep=";", encoding="utf-8-sig")
    df["ev"] = f[-8:-4]
    dfs.append(df)

# --- Összefűzés ---
data = pd.concat(dfs, ignore_index=True)

# --- Unnamed oszlopok törlése ---
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# --- Megye oszlop külön kezelése ---
megye_col = data["Megye"].astype(str)

# --- Tisztítás: minden whitespace eltávolítása a TÖBBI oszlopból ---
for col in data.columns:
    if col != "Megye":  # <<< NE nyúljunk a Megye oszlophoz
        data[col] = (
            data[col]
            .astype(str)
            .str.replace(r'\s+', '', regex=True)
            .str.replace(',', '.')
        )
        data[col] = pd.to_numeric(data[col], errors='coerce')

# --- Megye visszaállítása ---
data["Megye"] = megye_col

# --- Megye kódolása ---
data["Megye_kod"] = data["Megye"].astype("category").cat.codes

# --- Ellenőrzés ---
print(data.head())

# --- Csak numerikus oszlopok kiválasztása ---
numeric_columns = data.select_dtypes(include=['int', 'float'])
new_data = data[numeric_columns.columns]

# --- Korreláció ---
corr_matrix = new_data.corr()

# --- Heatmap ---
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap (2023 + 2024, Megye kódolva)')
plt.show()
