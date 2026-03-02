import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
df = pd.read_csv(
    r"adatbazisok\stadat-nep0034-22.1.2.1-hu.csv",
    sep=";",
    encoding="cp1250",
    header=1
)

print(df.columns.tolist())
