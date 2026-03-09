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
    df["ev"] = f[-8:-4]  # év kiemelése a fájlnévből
    dfs.append(df)

# --- Összefűzés ---
data = pd.concat(dfs, ignore_index=True)

# --- Unnamed oszlopok törlése ---
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# --- Megye oszlop külön kezelése ---
megye_col = data["Megye"].astype(str)

# --- Tisztítás: whitespace eltávolítása minden más oszlopból ---
for col in data.columns:
    if col != "Megye":  # <<< Megye oszlophoz nem nyúlunk
        data[col] = (
            data[col]
            .astype(str)
            .str.replace(r'\s+', '', regex=True)  # kezeli a 19 122 típusú számokat
            .str.replace(',', '.')
        )
        data[col] = pd.to_numeric(data[col], errors='coerce')

# --- Megye visszaállítása ---
data["Megye"] = megye_col

# --- Per capita mutatók ---
data['Autó/fő'] = data['auto allomany'] / data['Nepesseg']
data['Új autó/fő'] = data['uj auto'] / data['Nepesseg']
data['Használt autó/fő'] = data['hasznalt'] / data['Nepesseg']

# --- Megyék rangsorolása átlagkereset alapján ---
kereset_rang = (
    data.groupby("Megye")["atlag kereset"]
    .mean()
    .sort_values()
    .reset_index()
)

# Rang hozzárendelése (1 = legalacsonyabb kereset)
kereset_rang["Vármegye"] = kereset_rang["atlag kereset"].rank(method="dense").astype(int)

# Visszacsatolás a fő táblába
data = data.merge(kereset_rang[["Megye", "Vármegye"]], on="Megye", how="left")

# --- Csak numerikus oszlopok kiválasztása ---
numeric_columns = data.select_dtypes(include=['int', 'float']).columns.tolist()

# Biztosan benne legyen a Megye_kod
if "Vármegye" not in numeric_columns:
    numeric_columns.append("Vármegye")

new_data = data[numeric_columns]

# --- Szép magyar feliratok ---
label_map = {
    "Nepesseg": "Népesség",
    "atlag kereset": "Átlagkereset",
    "auto allomany": "Autóállomány",
    "uj auto": "Új autó",
    "hasznalt": "Használt autó",
    "eletkor": "Átlag életkor",
    "ev": "Év"
}

# --- Korreláció ---
corr_matrix = new_data.corr()
corr_matrix_renamed = corr_matrix.rename(index=label_map, columns=label_map)

plt.figure(figsize=(9, 7))

sns.heatmap(
    corr_matrix_renamed,
    annot=True,
    cmap='icefire',
    linewidths=0.5,
    annot_kws={"size": 8}  # kisebb számok a cellákban
)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.title('Korrelációs heatmap', fontsize=12, pad=3)

plt.tight_layout()
plt.subplots_adjust(top=0.92, bottom=0.08)

plt.show()
