import pandas as pd
import matplotlib.pyplot as plt

# A tényleges fejléc a CSV 2. vagy 3. sorában van, számold 0-tól
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",        # pontosvessző a magyar Excel CSV-knél
    encoding="latin1",
    header=1        # 0-tól számítva a 2. sor lesz a fejléc
)

# Tegyük fel, hogy az 1. sor kel
sor = atlagoskor.iloc[4]

# Csak a járműtípus oszlopok kellenek (pl. Személygépkocsi–Vontató)
oszlopok = ["Személygépkocsi"]
ertekek = sor[oszlopok]

# Grafikon készítése
plt.figure(figsize=(10,6))
plt.bar(oszlopok, ertekek)
plt.title(f"Járművek száma - {sor['Időszak']} ({sor['Év']})")
plt.ylabel("Darabszám")
plt.show()