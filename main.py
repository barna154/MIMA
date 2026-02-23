import pandas as pd
import matplotlib.pyplot as plt

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# 5. sor kiválasztása
sor = atlagoskor.iloc[4]

# Járműoszlopok
oszlopok = ["Személygépkocsi", "Autóbusz", "Motorkerékpár", "Tehergépkocsi", "Vontató"]

# Értékek számmá alakítása
ertekek = sor[oszlopok].str.replace(' ', '').astype(int)

# Rendezés érték szerint csökkenő sorrendben
ertekek_sorted = ertekek.sort_values(ascending=False)

# Grafikon
plt.figure(figsize=(10,6))
plt.bar(ertekek_sorted.index, ertekek_sorted.values)
plt.title(f"Járművek száma - {sor['Időszak']} ({sor['Év']})")
plt.ylabel("Darabszám")
plt.show()