# Off the Sheet 02 · We set a trap for an AI

Two tiny files, one hidden problem, and one line that catches it.

`prices.csv` lists **Widget twice** (same product, same price, typed in two times).
A plain join does not complain. It quietly counts every Widget order twice.

| | rows after the join | total revenue |
|---|---|---|
| Plain join (`trap.py`) | 9 (should be 6) | **1564.5** (30% too high, no error) |
| The real answer (`fix.py`) | 6 | **1203.5** |

## Run it

```bash
pip install pandas
python trap.py        # 6 orders in, 9 rows out, 1564.5  <- wrong, and no error
python ai_answer.py   # stops with a MergeError          <- the seatbelt working
python fix.py         # shows the duplicate, then 1203.5 <- correct
```

## The files

| File | What it is |
|---|---|
| `sales.csv` | 6 orders |
| `prices.csv` | the bait: Widget is in there twice |
| `PROMPT.txt` | the exact request we gave the AI |
| `trap.py` | the plain join that falls into the trap |
| `ai_answer.py` | what OpenAI's Codex wrote, unedited |
| `fix.py` | find the duplicate, remove it, keep the check |

## The seatbelt

```python
orders = sales.merge(prices, on="product", how="left", validate="many_to_one")
```

`validate="many_to_one"` (short form: `validate="m:1"`) tells pandas: many sales
rows may share a product, but each product may appear only **once** in the price
list. If that is not true, pandas stops with a `MergeError` instead of handing
you a wrong number.

This is stop 7, "I want to combine two tables", on page 7 of The Python Line Map.

## The rule

When a check fails, do not delete the check to make the error go away.
Fix the data. The error is the message.

`fix.py` uses `drop_duplicates()`, which removes rows that are exact copies. If
Widget were listed twice with two *different* prices, the check would still stop
you, and it should: someone has to decide which price is right.

## Honest notes

- This was **one AI and one run**: OpenAI's Codex, pandas 2.2.3, Python 3.12.
  It is not a benchmark. Another assistant, or the same one on another day, may
  write the plain join.
- The AI was asked to write the script from `PROMPT.txt` alone, save it, and not
  change it after seeing the result. The instructions it received also said this
  was a test, which may have made it more careful than usual.
- The error text changes between pandas versions. pandas 2.2 says
  `Merge keys are not unique in right dataset; not a many-to-one merge`;
  pandas 3 adds a list of the duplicated keys. The totals are the same.

## Try it on your AI

Paste `PROMPT.txt` into your favourite assistant, save its answer next to the
two CSV files, run it, and compare:

- `1203.5` or an error about duplicate keys: it buckled up.
- `1564.5`: it fell into the trap.

Video: Runtime Explained on YouTube, playlist "Off the Sheet".
