import pandas as pd 

atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",          # mert valószínűleg pontosvesszős
    encoding="latin1",  # Windows-1250 / latin1 a magyar CSV-kné
)

otodik_sor = atlagoskor.iloc[2]  

print(otodik_sor)