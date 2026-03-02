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

# Magyarország összesen sor kiválasztása (személygépkocsi blokk)
mask = (df["Területi egység neve"] == "Magyarország összesen") & \
       (df["Területi egység szintje"] == "ország")

orszagos = df[mask].iloc[0]

# Évek kigyűjtése (2000–2024)
evszamok = [str(ev) for ev in range(2000, 2025)]

# Értékek átalakítása
ertekek = (
    orszagos[evszamok]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# Diagram
plt.figure(figsize=(14, 7), facecolor="#DEDCDC")
x_pos = range(len(evszamok))

colors = ["#8BF43F", "green"]
plt.bar(x_pos, ertekek, color=colors)

# Feliratok az oszlopok tetején
for i, v in enumerate(ertekek):
    plt.text(
        i,
        v * 0.6,
        f"{v:,}".replace(",", " "),
        ha="center",
        va="center",
        fontsize=15,
        color="black",
        fontweight="bold",
        rotation=90
    )

plt.title("Magyarország teljes személygépkocsi-állománya (2000–2024)",
          color="black", size=23, fontweight="bold")

plt.xlabel("Év", color="black", size=20, fontweight="bold")
plt.ylabel("Darabszám", color="black", size=20, fontweight="bold")

plt.xticks(x_pos, evszamok, rotation=45)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().tick_params(axis="x", colors="black")
plt.gca().tick_params(axis="y", colors="black")
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
