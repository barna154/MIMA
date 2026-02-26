import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# --- ÁTLAGÉLETKOR TÁBLA BEOLVASÁSA ---

# Újra beolvassuk a CSV-t, mert az előző részben levágtuk a végét
eletkor_df = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",
    encoding="cp1250",
    header=1
)

eletkor_df.columns = eletkor_df.columns.str.strip()
def keres_oszlop(df, kulcsszavak):
    kulcsszavak = [k.lower() for k in kulcsszavak]
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in kulcsszavak):
            return col
    raise ValueError(f"Nincs ilyen oszlop: {kulcsszavak}")

eletkor_df.columns = eletkor_df.columns.str.strip()

# Megkeressük az "átlagos kor" blokk kezdetét
start_index = eletkor_df[eletkor_df[eletkor_df.columns[0]].astype(str).str.contains("tlagos", case=False, na=False)].index

# Ha megtaláltuk, levágjuk előtte lévő sorokat
if len(start_index) > 0:
    eletkor_df = eletkor_df.loc[start_index[0]+1:]

# Oszlopok felismerése
oszlop_ev2 = keres_oszlop(eletkor_df, ["ev"])
oszlop_idoszak2 = keres_oszlop(eletkor_df, ["ido"])
oszlop_kor = keres_oszlop(eletkor_df, ["kor"])

# Év kitöltése
eletkor_df[oszlop_ev2] = eletkor_df[oszlop_ev2].ffill()

# Csak szám típusú sorok
eletkor_sorok = eletkor_df[
    eletkor_df[oszlop_kor]
    .astype(str)
    .str.replace(",", ".")
    .str.replace(" ", "")
    .str.replace("-", "")
    .str.replace("nan", "")
    .str.replace("NaN", "")
    .str.replace("n.a.", "")
    .str.replace("n.a", "")
    .str.replace("..", "")
    .str.replace(".", "", 1)
    .str.isdigit()
]

# Átalakítás float-ra
eletkor_sorok[oszlop_kor] = (
    eletkor_sorok[oszlop_kor]
    .astype(str)
    .str.replace(",", ".")
    .astype(float)
)

# Csak június 30.
jun_kor = eletkor_sorok[
    eletkor_sorok[oszlop_idoszak2].str.contains("30.", na=False)
]

# X és Y adatok
x_labels2 = jun_kor[oszlop_ev2].astype(str).str.replace(".", "", regex=False).tolist()
y2 = jun_kor[oszlop_kor].tolist()

# --- ÁTLAGÉLETKOR DIAGRAM ---
plt.figure(figsize=(12, 7), facecolor="#DEDCDC")
x_pos2 = list(range(len(x_labels2)))

plt.bar(x_pos2, y2, color="#8BF43F")

for i, v in enumerate(y2):
    plt.text(
        x_pos2[i],
        v + max(y2)*0.01,
        f"{v:.1f}",
        ha="center",
        va="bottom",
        fontsize=12,
        color="black",
        fontweight="bold"
    )

plt.title("Személygépkocsik átlagéletkora június végén", color="black", size="23", fontweight="bold")
plt.xlabel("Év", color="black", size="20", fontweight="bold")
plt.ylabel("Év (átlagéletkor)", color="black", size="20", fontweight="bold")
plt.xticks(x_pos2, x_labels2)
plt.gca().tick_params(axis="x", colors="black")
plt.gca().tick_params(axis="y", colors="black")
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")
plt.tight_layout()
plt.show()
