import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="cp1250",   # magyar karakterek
    header=1
)

# Oszlopnevek tisztítása (szóköz eltávolítás)
atlagoskor.columns = atlagoskor.columns.str.strip()

# Megkeressük a tényleges oszlopneveket
oszlop_szemely = [c for c in atlagoskor.columns if 'Személygépkocsi' in c][0]
oszlop_ev = [c for c in atlagoskor.columns if 'Év' in c or 'Ev' in c][0]
oszlop_idoszak = [c for c in atlagoskor.columns if 'Időszak' in c or 'Idoszak' in c or 'Idõszak' in c][0]

# Hiányzó 'Év' kitöltése az előző sorral
atlagoskor[oszlop_ev] = atlagoskor[oszlop_ev].ffill()

# Csak a darabszám sorok (átlagos kor sorokat kihagyjuk)
darabszam_sorok = atlagoskor[
    atlagoskor[oszlop_szemely].astype(str).str.replace(' ','').str.replace(',','').str.isdigit()
]

# Konvertálás int-re
darabszam_sorok[oszlop_szemely] = darabszam_sorok[oszlop_szemely].astype(str).str.replace(' ','').astype(int)

# Csak júniusi sorok
jun_sorok = darabszam_sorok[
    darabszam_sorok[oszlop_idoszak].str.contains('június', na=False)
]

# X és Y adatok
x = jun_sorok[oszlop_ev].astype(str).str.replace('.', '', regex=False)
y = jun_sorok[oszlop_szemely]

# Grafikon készítése
plt.figure(figsize=(12,6))
plt.plot(x, y, marker='o', linestyle='-', color='blue')
plt.title("Személygépkocsik száma június végén")
plt.xlabel("Év")
plt.ylabel("Darabszám")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))  # teljes számok
plt.grid(True)
plt.show()