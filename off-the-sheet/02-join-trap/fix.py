# The fix: find the repeated price, remove it, keep the seatbelt on.
import pandas as pd

sales = pd.read_csv("sales.csv")
prices = pd.read_csv("prices.csv")

print(prices[prices.duplicated()])        # which prices are duplicated?
prices = prices.drop_duplicates()

orders = sales.merge(prices, on="product", how="left", validate="many_to_one")
print((orders["units"] * orders["price"]).sum())
