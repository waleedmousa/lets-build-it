# The trap: a plain join. No error, no warning, wrong total.
import pandas as pd

sales = pd.read_csv("sales.csv")
prices = pd.read_csv("prices.csv")
orders = sales.merge(prices, on="product")

print(len(sales), "orders in,", len(orders), "rows out")
print((orders["units"] * orders["price"]).sum())
