# Homework: scale it up a little

In the video, the model reads **one** file. Your job:

1. **Point it at a whole folder of your own files.**
2. **Print which file each answer came from.**

No full solution here on purpose. Three hints are enough.

## Hint 1: read every file in a folder

```python
from pathlib import Path

for f in Path("docs").glob("*.md"):
    text = f.read_text(encoding="utf-8")
    ...
```

Put a few `.md` or `.txt` files in a `docs` folder first.

## Hint 2: remember where each chunk came from

Keep a second list, the same length as `chunks`. When you add a chunk, add its file name to the other list:

```python
chunks, sources = [], []
...
chunks.append(c.strip())
sources.append(f.name)
```

## Hint 3: carry the source through `retrieve`

`best` already holds the positions of the winning chunks. Use the same positions to look up the file names, and return both. Then print the file names after the answer.

## How you know it works

Ask a question whose answer is in only one of your files. The printed file name should be that file.

## Want more? The three upgrades from the video

| Upgrade | Why | Where to start |
|---|---|---|
| Store the vectors | Right now every run embeds everything again | `np.save("vectors.npy", vectors)` and `np.load`, then a vector database: see [`../vector-databases`](../vector-databases) |
| Overlap your chunks | So an answer is never cut in half, like "Gradient" was | Make each chunk start a little before the previous one ended |
| Re-rank | So the right page comes first, not the one that only sounds right | Retrieve 10, then ask the model which 3 really answer the question |

Tell us what you made it read in the comments of the video.
