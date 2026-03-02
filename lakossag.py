import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 1) Beolvasás header=1
df = pd.read_csv(
    r"adatbazisok/stadat-nep0034-22.1.2.1-hu.csv",
    sep=";",
    encoding="cp1250",
    header=1
)

# 2) Összesen sor megtalálása
start = df.index[df["Területi egység neve"] == "Összesen"][0] + 1

# 3) Ország összesen sor megtalálása
end = df.index[df["Területi egység neve"].str.startswith("Ország")][0] - 1

# 4) Kivágjuk a megyéket + Budapestet tartalmazó részt
osszes = df.loc[start:end].copy()

# 5) Csak megyék + Budapest
mask = (
    osszes["Területi egység szintje"].str.contains("vármegye", case=False, na=False) |
    osszes["Területi egység szintje"].str.contains("főváros", case=False, na=False)
)
osszes = osszes[mask].copy()

# 6) 2024 tisztítása
osszes["2024"] = (
    osszes["2024"]
    .astype(str)
    .str.replace(" ", "", regex=False)
    .astype(int)
)

# 7) Rendezés
osszes = osszes.sort_values("2024", ascending=False)

# 8) Diagram
plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

x_labels = osszes["Területi egység neve"]
y_values = osszes["2024"]
x_pos = range(len(x_labels))

plt.bar(x_pos, y_values, color="#8BF43F")

max_val = max(y_values)

special = ["Budapest", "Pest"]

for i, (nev, v) in enumerate(zip(x_labels, y_values)):
    nev_clean = "".join(nev.split())

    if nev_clean in special:
        plt.text(i, v * 0.5, f"{v:,}".replace(",", " "),
                 ha="center", va="center", fontsize=15,
                 color="black", fontweight="bold", rotation=90)
    else:
        plt.text(i, v + max_val * 0.01, f"{v:,}".replace(",", " "),
                 ha="center", va="bottom", fontsize=15,
                 color="black", fontweight="bold", rotation=90)

plt.title("Lakónépesség vármegyénként (2024)", size=23, fontweight="bold")
plt.xlabel("Vármegye", size=20, fontweight="bold")
plt.ylabel("Fő", size=20, fontweight="bold")

plt.xticks(x_pos, x_labels, rotation=45, ha="right")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
