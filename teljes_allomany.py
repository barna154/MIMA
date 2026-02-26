import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV / TXT beolvasása
df = pd.read_csv(
    r"adatbazisok\stadat-sza0040-24.1.2.2-hu.csv",
    sep="\t",
    encoding="utf-8"
)

# Oszlopnevek tisztítása
df.columns = df.columns.str.strip()

# Magyarország összesen sor kiválasztása
orszagos = df[df[df.columns[0]].astype(str).str.contains("Magyarország összesen")].iloc[0]

# Évek és értékek kigyűjtése
evszamok = df.columns[2:]  # 2000–2024
ertekek = orszagos[2:].astype(str).str.replace(" ", "").astype(int)

# Diagram
plt.figure(figsize=(14, 7), facecolor="#DEDCDC")

x_pos = range(len(evszamok))

plt.bar(x_pos, ertekek, color="#8BF43F")

# Feliratok az oszlopok tetején
for i, v in enumerate(ertekek):
    plt.text(
        i,
        v + max(ertekek)*0.005,
        f"{v:,}".replace(",", " "),
        ha="center",
        va="bottom",
        fontsize=10,
        color="black",
        fontweight="bold"
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
