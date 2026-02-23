import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# Üres 'Év' kitöltése az előző évvel
atlagoskor['Év'] = atlagoskor['Év'].ffill()

# Csak a darabszám sorok: a 'Személygépkocsi' oszlopban van szám (átlagos kor sorokat hagyjuk ki)
# Általában az átlagos kor sor után egy "átlagos kor" cím van, ami NaN értékeket ad
darabszam_sorok = atlagoskor[atlagoskor['Személygépkocsi'].str.replace(' ', '').str.replace(',', '').str.isdigit()]

# Szóközök eltávolítása és int konvertálás
darabszam_sorok['Személygépkocsi'] = darabszam_sorok['Személygépkocsi'].str.replace(' ', '').astype(int)

# Csak júniusi sorok
jun_sorok = darabszam_sorok[darabszam_sorok['Időszak'].str.contains('június', na=False)]

# X és Y
x = jun_sorok['Év'].str.replace('.', '', regex=False)
y = jun_sorok['Személygépkocsi']

# Grafikon
plt.figure(figsize=(12,6))
plt.plot(x, y, marker='o')
plt.title("Személygépkocsik száma június végén")
plt.xlabel("Év")
plt.ylabel("Darabszám")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
plt.grid(True)
plt.show()