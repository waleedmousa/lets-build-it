# Vector Databases: teach a search bar to read

The code from the Runtime Explained short **"Vector Databases: Your Search Bar Can't Read. Let's Fix It."**

A customer writes *"I can't log in"*. Your support inbox already has the ticket *"Password reset link not working"*. Keyword search finds nothing, because the two sentences share no words. A vector database finds it, because it searches by meaning.

## Run it

You need Python 3.9 or newer.

```bash
pip install chromadb wordllama
python search.py
```

You should see:

```
Password reset link not working
0.78
```

The first line is the closest ticket. The second is the distance. Smaller means closer in meaning.

No account, no API key. Everything runs on your machine. The first run downloads one small tokenizer file for the model.

## What the three steps do

| Step | Line in `search.py` | In plain words |
|---|---|---|
| 1 | `vectors = model.embed(tickets)` | Each ticket becomes 256 numbers. Think of them as coordinates on a map of meaning. |
| 2 | `db.add(ids=ids, documents=tickets, embeddings=vectors)` | Chroma stores each ticket next to its coordinates. |
| 3 | `db.query(query_embeddings=model.embed([question]), n_results=1)` | The question gets coordinates the same way, and Chroma returns whoever lives closest. |

## See keyword search fail first

```bash
python keyword_vs_vector.py
```

It asks four questions two ways. Keyword search returns an empty list every time. The vector database returns the right ticket every time:

| Question | Keyword search | Vector database (closest) | Distance |
|---|---|---|---|
| I can't log in | nothing | Password reset link not working | 0.78 |
| money taken from my card two times | nothing | Charged twice for my subscription | 0.73 |
| where is my money back? | nothing | Refund still not received after 10 days | 0.80 |
| the app keeps closing | nothing | App crashes when I upload a photo | 0.79 |

## Make it yours

1. Replace the `tickets` list with your own text: notes, docs, FAQ answers, product names.
2. Change `question` to something in your own words.
3. Raise `n_results` to get the top 3 or top 5 instead of the single best match.

## Good to know

- **Tested with** Python 3.13, chromadb 1.5.9 and wordllama 0.3.9. Other versions should work, but your distances may differ slightly.
- **WordLlama is a small, fast model.** It is perfect for learning. For a real product, try a stronger embedding model and compare the results on your own data.
- **`chromadb.Client()` keeps everything in memory.** Use `chromadb.PersistentClient(path="./db")` to save your data to disk.
- **The map in the video is a picture.** The real space has 256 dimensions. The video flattens it to 2 so you can see it.

## Where this is used

Chatbots that answer from your documents (RAG), product search, recommendations and duplicate ticket detection all start with this same step: find the closest pieces of text.
