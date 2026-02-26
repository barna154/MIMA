import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"adatbazisok\24.1.2.2. A közúti gépjárművek száma vármegye és r.txt",
    sep=";",
    encoding="cp1250"  # ha így jó a magyar ékezet
)

# Csak a 'Magyarország összesen' sor, személygépkocsi blokk
mask_total = (df["Területi egység neve"] == "Magyarország összesen") & \
             (df["Területi egység szintje"] == "ország")

total_row = df[mask_total].iloc[0]

years = [str(y) for y in range(2000, 2025)]
values = (
    total_row[years]
    .astype(str)
    .str.replace(" ", "", regex=False)  # ezredelés szóköz eltávolítása
    .astype(int)
)

plt.figure(figsize=(12, 6))
plt.bar(years, values)
plt.xticks(rotation=45)
plt.title("Személygépkocsik száma Magyarországon (dec. 31., 2000–2024)")
plt.ylabel("Darabszám")

plt.tight_layout()
plt.show()
