import pandas as pd
import matplotlib.pyplot as plt

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1
)


print(atlagoskor.iloc[1])
# Szóközök eltávolítása az oszlopnevekből
atlagoskor.columns = atlagoskor.columns.str.strip()

# Az 5. sor kiválasztása (index 4)
sor = atlagoskor.iloc[3]

# Csak a járműtípus oszlopok kellenek
oszlopok = ["Személygépkocsi", "Autóbusz", "Motorkerékpár", "Tehergépkocsi", "Vontató"]
ertekek = sor[oszlopok]

# Grafikon készítése
plt.figure(figsize=(10,6))
plt.bar(ertekek, oszlopok)
plt.title(f"Járművek száma - ({sor['Év']})")
plt.ylabel("Darabszám")
plt.show()