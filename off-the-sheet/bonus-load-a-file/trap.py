import pandas as pd

df = pd.read_csv("sales.csv")
print(df.dtypes)
print(df["date"].dt.month)
