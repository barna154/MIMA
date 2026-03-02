import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
df = pd.read_csv(
    r"adatbazisok\stadat-nep0034-22.1.2.1-hu.csv",
    sep=";",
    encoding="iso-8859-2",   # <<< EZ A LÉNYEG
    header=1
)

df.columns = df.columns.str.strip()
print(df.columns.tolist())
