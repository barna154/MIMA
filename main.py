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
atlagoskor.columns = atlagoskor.columns.str.strip()
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
stop_index = atlagoskor[atlagoskor[oszlop_ev].astype(str).str.contains("tlagos", case=False, na=False)].index

if len(stop_index) > 0:
    atlagoskor = atlagoskor.loc[:stop_index[0]-1]

atlagoskor[oszlop_ev] = atlagoskor[oszlop_ev].ffill()
darabszam_sorok = atlagoskor[
    atlagoskor[oszlop_szemely]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", "")
    .str.isdigit()
]

darabszam_sorok[oszlop_szemely] = (
    darabszam_sorok[oszlop_szemely]
    .astype(str)
    .str.replace(" ", "")
    .str.replace(",", "")
    .astype(int)
)

jun_sorok = darabszam_sorok[
    darabszam_sorok[oszlop_idoszak].str.contains("30.", na=False)
]
x_labels = jun_sorok[oszlop_ev].astype(str).str.replace(".", "", regex=False).tolist()
y = jun_sorok[oszlop_szemely].tolist()




# Diagram
plt.figure(figsize=(12, 7), facecolor="#DEDCDC")
x_pos = list(range(len(x_labels)))
colors = ["#8BF43F", "green"]
plt.bar(x_pos, y, color=colors)
for i, v in enumerate(y):
    plt.text(
        x_pos[i],
        v + max(y)*0.01,
        f"{v:,}".replace(",", " "),
        ha="center",
        va="bottom",
        fontsize=12,
        color="black"
    )

plt.title("Személygépkocsik száma június végén", color="black", size="23", fontweight="bold")
plt.xlabel("Év", color="black", size="20", fontweight="bold")
plt.ylabel("Darabszám", color="black", size="20", fontweight="bold")
plt.xticks(x_pos, x_labels)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().tick_params(axis="x", colors="black") 
plt.gca().tick_params(axis="y", colors="black")
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")
plt.tight_layout()
plt.show()
