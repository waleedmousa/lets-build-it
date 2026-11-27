import pandas as pd

df = pd.read_csv("big_sales.csv")
south = df[df["region"] == "South"]
print(south["units"].sum())
