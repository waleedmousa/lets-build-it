import polars as pl

lf = pl.scan_csv("big_sales.csv")
answer = (lf
  .filter(pl.col("region") == "South")
  .select(pl.col("units").sum())
  .collect())
print(answer.item())
