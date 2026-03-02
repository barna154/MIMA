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

# A személygépkocsi blokk kivágása
start = df.index[df["Területi egység neve"] == "Személygépkocsi"][0] + 1
end = df.index[df["Területi egység neve"] == "Autóbusz"][0] - 1

szemelyauto_df = df.loc[start:end].copy()

# Budapest + minden vármegye
mask = (
    szemelyauto_df["Területi egység szintje"].str.contains("vármegye", na=False)
    | (szemelyauto_df["Területi egység neve"] == "Budapest")
)

szemelyauto_df = szemelyauto_df[mask]


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

colors = ["#8BF43F", "green"]
plt.bar(x_pos, y_values, color=colors)

# Feliratok az oszlopokon belül
for i, v in enumerate(y_values):
    plt.text(
        x_pos[i],
        v + max(y_values)*0.01,
        f"{v:,}".replace(",", " "),
        ha="center",
        va="bottom",
        fontsize=15,
        color="black",
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
