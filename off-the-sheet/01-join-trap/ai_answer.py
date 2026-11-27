import pandas as pd

sales = pd.read_csv("sales.csv")
prices = pd.read_csv("prices.csv")
orders = sales.merge(prices, on="product", how="left", validate="many_to_one")

if orders[["units", "price"]].isna().any().any():
    raise ValueError("Every sale needs a unit count and a matching price.")

print((orders["units"] * orders["price"]).sum())
