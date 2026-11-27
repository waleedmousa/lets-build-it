# Off the Sheet, bonus: I want to load a file

**Cheat sheet:** The Python Line Map, page 7, Data Analyst line, stop 1.

One box from the cheat sheet, used for real. Three levels: load a file, load it with real dates, and scan a huge file without reading all of it.

## Set up once

You need [uv](https://docs.astral.sh/uv/). Then:

```
uv init --no-package load-a-file
cd load-a-file
uv add pandas polars pyarrow
```

Copy the files from this folder into `load-a-file`.

## Level 1: Start here

```
uv run level1.py
```

```
         date   region product  units  price
0  2026-01-05   north   Widget   12.0    9.5
1  2026-01-06    South  Gadget   30.0   20.0
2  2026-01-06    South  Widget    NaN    9.5
3  2026-02-03     East  Widget   18.0    9.5
4  2026-02-03     East  Widget   18.0    9.5
```

Five rows, five columns. That is a DataFrame: a table Python can work with.

## The trap

```
uv run trap.py
```

It prints the column types, then fails on purpose:

```
date           str
...
AttributeError: Can only use .dt accessor with datetimelike values
```

The `date` column is `str`, which means text. It looks like a date, but Python cannot ask text for its month.

## Level 2: Daily use

```
uv run level2.py
```

```
date       datetime64[us]
...
[1, 1, 1, 2, 2]
['Monday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday']
29 days 00:00:00
```

One extra piece, `parse_dates=["date"]`, and the same file now has real dates: you can ask for the month, the weekday, or the time between two sales.

## Level 3: 2026, when the file gets huge

First make a big file (5 million rows, about 151 MB, takes under a minute):

```
uv run make_big.py
```

Then answer the same question two ways: total units sold in the South.

```
uv run level3_pandas.py
uv run level3_polars.py
```

Both print `25015657`.

The difference is how they get there. pandas reads the whole file into memory first. `pl.scan_csv` reads nothing: it waits until it knows your question, then reads only the two columns the question needs, and only when you call `.collect()`.

To see the cost of each on your machine (Mac and Linux only):

```
uv run measure.py
```

What we measured:

| | pandas `read_csv` | Polars `scan_csv` |
|---|---|---|
| Columns read | 5 of 5 | 2 of 5 |
| Time | about 0.9 s | about 0.4 s |
| Peak memory | about 690 MB | about 250 MB |

Your numbers will differ with your machine and versions. One thing we found while testing: without `pyarrow` installed, pandas took about 1.8 s and 520 MB on the same file, so the gap in time grew and the gap in memory shrank. Polars stayed the same.

## Your turn

Type it, don't copy it. Load one of your own files and check the types:

```python
import pandas as pd

df = pd.read_csv("your_file.csv")
print(df.dtypes)
```

Is your date really a date? If it says `str`, add `parse_dates=["your_date_column"]`.

## What we tested before publishing

- Every command above was run in a fresh `uv` project, exactly as written, and gave the output shown.
- Versions: Python 3.14 and 3.13, pandas 3.1.1, Polars 2.1.0, pyarrow 26.0, uv 0.11.
- `make_big.py` uses a fixed random seed, so your big file and your answer will match ours.
- Tested on Linux. `measure.py` relies on a module Windows does not have; everything else is plain Python.
