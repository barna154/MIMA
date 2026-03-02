import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
df = pd.read_csv(
    r"adatbazisok/stadat-nep0034-22.1.2.1-hu.csv",
    sep=";",          # a KSH népesség CSV általában pontosvesszős
    encoding="utf-8",
    header=0
)

# Csak a megyék sorai (kiszűrjük a régiókat, országot, összesítéseket)
# A megyék szintje általában "vármegye" vagy "megye"
mask = df["Területi egység szintje"].str.contains("megye", case=False, na=False)
megye_df = df[mask].copy()

# 2024-es lakosság kivétele
megye_df["2024"] = (
    megye_df["2024"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# Rendezés csökkenő sorrendben
megye_df = megye_df.sort_values("2024", ascending=False)

# Diagram
plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

x_labels = megye_df["Területi egység neve"]
y_values = megye_df["2024"]
x_pos = range(len(x_labels))

plt.bar(x_pos, y_values, color="#8BF43F")

# Feliratok az oszlopokon
max_val = max(y_values)

for i, (nev, v) in enumerate(zip(x_labels, y_values)):
    nev_clean = "".join(nev.split())  # whitespace normalizálás

    if nev_clean in ["Budapest", "Pest"]:
        # magas oszlopok → belső felirat
        plt.text(
            i,
            v * 0.5,
            f"{v:,}".replace(",", " "),
            ha="center",
            va="center",
            fontsize=15,
            color="black",
            fontweight="bold",
            rotation=90
        )
    else:
        # normál megyék → felirat fölé
        plt.text(
            i,
            v + max_val * 0.01,
            f"{v:,}".replace(",", " "),
            ha="center",
            va="bottom",
            fontsize=15,
            color="black",
            fontweight="bold",
            rotation=90
        )

plt.title("Lakónépesség vármegyénként (2024)", 
          color="black", size=23, fontweight="bold")

plt.xlabel("Vármegye", color="black", size=20, fontweight="bold")
plt.ylabel("Fő", color="black", size=20, fontweight="bold")

plt.xticks(x_pos, x_labels, rotation=45, ha="right")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
