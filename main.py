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

# --- Automatikus oszlopfelismerés ---
def keres_oszlop(df, kulcsszavak):
    kulcsszavak = [k.lower() for k in kulcsszavak]
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in kulcsszavak):
            return col
    raise ValueError(f"Nincs ilyen oszlop: {kulcsszavak}")

oszlop_szemely = keres_oszlop(atlagoskor, ["szem"])
oszlop_ev = keres_oszlop(atlagoskor, ["ev"])
oszlop_idoszak = keres_oszlop(atlagoskor, ["ido"])

# --- A darabszám blokk levágása az "átlagos kor" sor előtt ---
stop_index = atlagoskor[atlagoskor[oszlop_ev].astype(str).str.contains("tlagos", case=False, na=False)].index

if len(stop_index) > 0:
    atlagoskor = atlagoskor.loc[:stop_index[0]-1]

# Hiányzó év kitöltése
atlagoskor[oszlop_ev] = atlagoskor[oszlop_ev].ffill()

# Csak darabszám sorok
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

# --- Júniusi sorok kiválasztása: "30." dátum alapján ---
jun_sorok = darabszam_sorok[
    darabszam_sorok[oszlop_idoszak].str.contains("30.", na=False)
]

# X és Y adatok
x_labels = jun_sorok[oszlop_ev].astype(str).str.replace(".", "", regex=False).tolist()
y = jun_sorok[oszlop_szemely].tolist()

# --- Oszlopdiagram ---
plt.figure(figsize=(12, 6), facecolor="gray")

# X pozíciók (indexek!)
x_pos = list(range(len(x_labels)))

plt.bar(x_pos, y, color="green")

# Értékek kiírása az oszlopok fölé
for i, v in enumerate(y):
    plt.text(
        x_pos[i],
        v + max(y)*0.01,
        f"{v:,}".replace(",", " "),
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.title("Személygépkocsik száma június végén")
plt.xlabel("Év")
plt.ylabel("Darabszám")
plt.xticks(x_pos, x_labels)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
