import pandas as pd

# A tényleges fejléc a CSV 2. vagy 3. sorában van, számold 0-tól
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",        # pontosvessző a magyar Excel CSV-knél
    encoding="latin1",
    header=1        # 0-tól számítva a 2. sor lesz a fejléc
)

# Ellenőrzés: oszlopok nevei
print("Oszlopok:", atlagoskor.columns.tolist())

# Például egy konkrét oszlop
print(atlagoskor["Év"].head())