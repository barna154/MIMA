import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

adatok = {
    "Budapest": (723372/1686222)*1000,
    "Pest": (663795/1333257)*1000,
    "Győr-Moson-Sopron": (233647/473246)*1000,
    "Nógrád": (77296/180469)*1000,
    "Vas": (125725/248199)*1000,
    "Zala": (129933/260124)*1000,
    "Bács-Kiskun": (237645/491632)*1000,
    "Borsod-Abaúj-Zemplén": (229632/617800)*1000,
    "Szabolcs-Szatmár-Bereg": (206134/524513)*1000,
    "Hajdú-Bihar": (203438/520550)*1000,
    "Fejér": (198532/419490)*1000,
    "Csongrád-Csanád": (162099/389411)*1000,
    "Veszprém": (160122/335979)*1000,
    "Baranya": (151855/353331)*1000,
    "Jász-Nagykun-Szolnok": (139445/353511)*1000,
    "Komárom-Esztergom": (138785/301834)*1000,
    "Somogy": (136603/292691)*1000,
    "Békés": (128290/310912)*1000,
    "Heves": (121660/285058)*1000,
    "Tolna": (94757/206398)*1000
}

# Átalakítás listává
x_labels = list(adatok.keys())
y_values = list(adatok.values())
x_pos = range(len(x_labels))

plt.figure(figsize=(16, 8), facecolor="#DEDCDC")

colors = ["#8BF43F", "green"]
plt.bar(x_pos, y_values, color=colors)

for i, v in enumerate(y_values):
    plt.text(
        x_pos[i],
        v + max(y_values)*0.01,
        f"{v:.1f}",
        ha="center",
        va="bottom",
        fontsize=12,
        color="black",
        fontweight="bold"
    )


plt.title("Saját adatokból készült diagram", 
          color="black", size=23, fontweight="bold")

plt.xlabel("Vármegye", color="black", size=20, fontweight="bold")
plt.ylabel("Érték", color="black", size=20, fontweight="bold")

plt.xticks(x_pos, x_labels, rotation=45, ha="right")
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
plt.gca().set_facecolor("#DEDCDC")
plt.grid(axis="y", linestyle="--", alpha=0.6, color="green")

plt.tight_layout()
plt.show()
