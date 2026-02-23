import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="cp1250",
    header=1
)

# Oszlopnevek tisztítása
atlagoskor.columns = atlagoskor.columns.str.strip()

# Üres 'Év' kitöltése
atlagoskor['Ev'] = atlagoskor['Ev'].ffill()

# Csak azok a sorok, ahol a Személygépkocsi oszlop **számot tartalmaz**  
# (előző próbálkozás helyett, regex használat)
darabszam_sorok = atlagoskor[atlagoskor['Személygépkocsi'].str.replace(' ', '').str.match(r'^\d+$', na=False)]

# Konvertálás int-re
darabszam_sorok['Személygépkocsi'] = darabszam_sorok['Személygépkocsi'].str.replace(' ', '').astype(int)

# Csak júniusi sorok
jun_sorok = atlagoskor[
    atlagoskor['Személygépkocsi'].str.replace(' ', '').str.match(r'^\d+$', na=False) &
    atlagoskor['Idoszak'].str.contains('június', na=False)
]# X és Y
x = jun_sorok['Ev'].str.replace('.', '', regex=False)
y = jun_sorok['Személygépkocsi']

# Grafikon
plt.figure(figsize=(12,6))
plt.plot(x, y, marker='o')
plt.title("Személygépkocsik száma június végén")
plt.xlabel("Ev")
plt.ylabel("Darabszám")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
plt.grid(True)
plt.show()