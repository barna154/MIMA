import pandas as pd
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="latin1",
    header=1,
    #skip_blank_lines=True
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# Üres 'Év' kitöltése az előző évvel
atlagoskor['Év'] = atlagoskor['Év'].ffill()

# Csak júniusi sorok (ha évi egyszeri adat kell)
jun_sorok = atlagoskor[atlagoskor['Időszak'].str.contains('június', na=False)]

# Értékek: Személygépkocsi számok
# Szóközök eltávolítása és int-re konvertálás
jun_sorok['Személygépkocsi'] = jun_sorok['Személygépkocsi'].astype(str).str.replace(' ', '').astype(int)

# X és Y
x = jun_sorok['Év'].str.replace('.', '', regex=False)  # a pontot eltávolítjuk az évszám végéről
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