import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
df = pd.read_csv(
    r"adatbazisok\stadat-sza0040-24.1.2.2-hu.csv",
    sep=";",
    encoding="cp1250",
    header=1
)

# Csak a személygépkocsi blokkot tartjuk meg
szemelyauto_df = df[df["Területi egység neve"] != "Személygépkocsi"]

# Csak a vármegyék (nem régiók, nem ország)
megye_df = szemelyauto_df[szemelyauto_df["Területi egység szintje"] == "vármegye"]

# 2024-es értékek kigyűjtése
megye_2024 = megye_df[["Területi egység neve", "2024"]].copy()

# Számformátum tisztítása
megye_2024["2024"] = (
    megye_2024["2024"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# Rendezés csökkenő sorrendben (szebb diagram)
megye_2024 = megye_2024.sort_values("2024", ascending=False)

# Diagram
plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

x_labels = megye_2024["Területi egység neve"]
y_values = megye_2024["2024"]
x_pos = range(len(x_labels))

plt.bar(x_pos, y_values, color="#8BF43F")

# Feliratok az oszlopokon belül, elforgatva
for i, v in enumerate(y_values):
    plt.text(
        i,
        v * 0.35,  # az oszlop alsó harmadába tesszük
        f"{v:,}".replace(",", " "),
        ha="center",
        va="center",
        fontsize=9,
        color="white",
        fontweight="bold",
        rotation=90
    )

plt.title("Személygépkocsi-állomány vármegyénként (2024)", 
          color="black", size=23, fontweight="bold")

plt.xlabel("Vármegye", color="black", size=20, fontweight="bold")
plt.ylabel("Darabszám", color="black", size=20, fontweight="bold")

plt.xticks(x_pos, x_labels, rotation=45, ha="right")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().tick_params(axis="x", colors="black")
plt.gca().tick_params(axis="y", colors="black")
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
