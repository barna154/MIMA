import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
df = pd.read_csv(
    r"adatbazisok\24.1.2.2.csv",
    sep="\t",          # a te fájlod TAB-os!
    encoding="utf-8",
)

# A kategória sorok megtalálása
start = df.index[df["Területi egység neve"] == "Személygépkocsi"][0] + 1
end = df.index[df["Területi egység neve"] == "Autóbusz"][0] - 1

# Csak a személygépkocsi blokk
szemelyauto_df = df.loc[start:end].copy()

# Csak a vármegyék
szemelyauto_df = szemelyauto_df[szemelyauto_df["Területi egység szintje"] == "vármegye"]

# 2024-es értékek
szemelyauto_df["2024"] = (
    szemelyauto_df["2024"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# Rendezés
szemelyauto_df = szemelyauto_df.sort_values("2024", ascending=False)

# Diagram
plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

x_labels = szemelyauto_df["Területi egység neve"]
y_values = szemelyauto_df["2024"]
x_pos = range(len(x_labels))

plt.bar(x_pos, y_values, color="#8BF43F")

# Feliratok az oszlopokon belül
for i, v in enumerate(y_values):
    plt.text(
        i,
        v * 0.35,
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
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
