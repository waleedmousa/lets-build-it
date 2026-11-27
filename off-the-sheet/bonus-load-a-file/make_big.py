import random, datetime
random.seed(1)
regions = ["North", "South", "East", "West"]
products = [("Widget", 9.5), ("Gadget", 20), ("Gizmo", 14.25)]
start = datetime.date(2022, 1, 1)
with open("big_sales.csv", "w") as f:
    f.write("date,region,product,units,price\n")
    for i in range(5_000_000):
        day = start + datetime.timedelta(days=random.randrange(1800))
        name, price = random.choice(products)
        f.write(f"{day},{random.choice(regions)},{name},{random.randrange(1, 40)},{price}\n")
