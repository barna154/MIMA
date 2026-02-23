import pandas as pd 

atlagoskor = pd.read_csv(
    r"adatbazisok\stadat-sza0069-24.2.1.21-hu.csv",
    sep=";",          # mert valószínűleg pontosvesszős
    encoding="latin1"  # Windows-1250 / latin1 a magyar CSV-knél
)

otodik_sor = atlagoskor.iloc[4]  

print(otodik_sor)

atlag_kor_oszlop = atlagoskor["Személygépkocsi"]
print(atlag_kor_oszlop)