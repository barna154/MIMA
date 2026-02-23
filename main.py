import pandas as pd
import matplotlib.pyplot as plt

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1,       # a tényleges fejléc sor
    skip_blank_lines=True
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# Az 5. sor kiválasztása (index 4)
sor = atlagoskor.iloc[4]

# Járműoszlopok kiválasztása (Darabszám)
oszlopok = ["Személygépkocsi", "Autóbusz", "Motorkerékpár", "Tehergépkocsi", "Vontató"]

# Értékek konvertálása int-re (szóközök eltávolítása)
ertekek = sor[oszlopok].str.replace(' ', '').astype(int)

# Rendezés csökkenő sorrendbe
ertekek_sorted = ertekek.sort_values(ascending=False)

# Grafikon készítése
plt.figure(figsize=(10,6))
plt.bar(ertekek_sorted.index, ertekek_sorted.values)
plt.title(f"Járművek száma - {sor['Időszak']} ({sor['Év']})")
plt.ylabel("Darabszám")
plt.show()