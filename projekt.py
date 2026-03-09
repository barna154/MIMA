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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Fájlok ---
files = [
    r"adatbazisok\adatok2023.csv",
    r"adatbazisok\adatok2024.csv"
]

dfs = []

for f in files:
    df = pd.read_csv(f, sep=";", encoding="cp1250")
    df["ev"] = f[-8:-4]   # év hozzáadása
    dfs.append(df)

# --- Összefűzés ---
data = pd.concat(dfs, ignore_index=True)

# --- Unnamed oszlopok törlése ---
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# --- Tisztítás: minden whitespace eltávolítása ---
for col in data.columns:
    data[col] = (
        data[col]
        .astype(str)
        .str.replace(r'\s+', '', regex=True)   # <<< EZ A FONTOS!
        .str.replace(',', '.')
    )
    data[col] = pd.to_numeric(data[col], errors='coerce')

# --- Ellenőrzés ---
print(data.head())

# --- Korreláció ---
numeric_columns = data.select_dtypes(include=['int', 'float'])
corr_matrix = numeric_columns.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap (2023 + 2024)')
plt.show()
