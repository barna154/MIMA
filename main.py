import pandas as pd

atlagoskor = pd.read_csv(r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv") 

print(atlagoskor.head())
print("Oszlopok:", atlagoskor.columns.tolist())