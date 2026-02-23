import pandas as pd
import matplotlib.pyplot as plt

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1,
    skip_blank_lines=True
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# Üres 'Év' kitöltése az előző évvel (forward fill)
atlagoskor['Év'] = atlagoskor['Év'].ffill()
# 5. sor kiválasztása
sor = atlagoskor.iloc[4]

# Járműoszlopok kiválasztása
oszlopok = ["Személygépkocsi", "Autóbusz", "Motorkerékpár", "Tehergépkocsi", "Vontató"]

# Értékek konvertálása int-re
ertekek = sor[oszlopok].astype(str).str.replace(' ', '').astype(int)

# Rendezés csökkenő sorrendben
ertekek_sorted = ertekek.sort_values(ascending=False)

# Grafikon
plt.figure(figsize=(10,6))
plt.bar(ertekek_sorted.index, ertekek_sorted.values)
plt.title(f"Járművek száma - {sor['Év']} ({sor['Időszak']})")
plt.ylabel("Darabszám")
plt.show()