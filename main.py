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

# --- Automatikus oszlopfelismerés hibás ékezetekkel is ---
def keres_oszlop(df, kulcsszavak):
    kulcsszavak = [k.lower() for k in kulcsszavak]
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in kulcsszavak):
            return col
    raise ValueError(f"Nincs ilyen oszlop: {kulcsszavak}")

# A CSV-ben így néznek ki az oszlopok:
# 'Ev', 'Idoszak', 'Szem�lyg�pkocsi', 'Aut�busz', ...

oszlop_szemely = keres_oszlop(atlagoskor, ["Szemelygepkocsi"])
oszlop_ev = keres_oszlop(atlagoskor, ["Év"])
oszlop_idoszak = keres_oszlop(atlagoskor, ["ido", "Időszak"])

# Hiányzó év kitöltése
atlagoskor[oszlop_ev] = atlagoskor[oszlop_ev].ffill()

# Csak darabszám sorok (számok)
darabszam_sorok = atlagoskor[
    atlagoskor[oszlop_szemely]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", "")
    .str.isdigit()
]

# Konvertálás int-re
darabszam_sorok[oszlop_szemely] = (
    darabszam_sorok[oszlop_szemely]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", "")
    .astype(int)
)

# Csak júniusi sorok
jun_sorok = darabszam_sorok[
    darabszam_sorok[oszlop_idoszak].str.contains("j\u00fanius", case=False, na=False)
]

# X és Y adatok
x = jun_sorok[oszlop_ev].astype(str).str.replace(".", "", regex=False)
y = jun_sorok[oszlop_szemely]

# Grafikon
plt.figure(figsize=(12, 6))
plt.plot(x, y, marker="o", linestyle="-", color="blue")
plt.title("Személygépkocsik száma június végén")
plt.xlabel("Év")
plt.ylabel("Darabszám")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.grid(True)
plt.tight_layout()
plt.show()
