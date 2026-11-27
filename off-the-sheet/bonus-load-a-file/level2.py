import pandas as pd

df = pd.read_csv("sales.csv",
    parse_dates=["date"])
print(df.dtypes)
print(df["date"].dt.month.tolist())
print(df["date"].dt.day_name().tolist())
print(df["date"].max() - df["date"].min())
