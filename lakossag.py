import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# CSV beolvasása
df = pd.read_csv(
    r"adatbazisok\stadat-nep0034-22.1.2.1-hu.csv",
    sep=";",
    encoding="cp1250",
    header=0
)

# --- OSZLOPNEVEK TISZTÍTÁSA ---
df.columns = df.columns.str.strip().str.replace("\ufeff", "", regex=False)

# --- Összesen blokk kivágása ---
start = df.index[df["Területi egység neve"] == "Összesen"][0] + 1

lakossag_df = df.loc[start:].copy()

# Csak Budapest + vármegyék
mask = (
    lakossag_df["Területi egység szintje"].str.contains("vármegye", na=False)
    | (lakossag_df["Területi egység neve"] == "Budapest")
)

lakossag_df = lakossag_df[mask]

# 2024-es értékek tisztítása
lakossag_df["2024"] = (
    lakossag_df["2024"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# Rendezés
lakossag_df = lakossag_df.sort_values("2024", ascending=False)

# Diagram
plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

x_labels = lakossag_df["Területi egység neve"]
y_values = lakossag_df["2024"]
x_pos = range(len(x_labels))

colors = ["#8BF43F", "green"]
plt.bar(x_pos, y_values, color=colors)

special = ["Budapest", "Pest"]

for i, (nev, v) in enumerate(zip(x_labels, y_values)):
    nev_clean = nev.strip()

    if nev_clean in special:
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
        plt.text(
            i,
            v + max(y_values) * 0.01,
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
