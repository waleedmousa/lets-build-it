# Chat with your own documents: RAG from scratch

The code from the Runtime Explained short on RAG (Let's Build It, EP 11).

**The problem.** Ask a model about your own company and it either says "I don't know" or makes something up, because it never read your documents. Retraining it for every new file is slow and expensive.

**The trick (RAG).** Before the model answers, find the right page and paste it into the question.

`rag.py` is the whole thing: **one file, 26 lines of code**, no framework, no vector database.

## Build it

You need Python 3.9 or newer and [Ollama](https://ollama.com) (free, runs on your own computer).

```bash
mkdir my-rag && cd my-rag          # 1. a folder
# 2. put a document in it: handbook.md from this repo, or your own
ollama pull llama3.2               # 3. the models
ollama pull nomic-embed-text
pip install ollama numpy           # 4. the libraries
# 5. create rag.py (copy it from this repo, or type it along with the video)
python rag.py
```

Then type a question at `Ask:`. Press Ctrl+C to stop.

```
Ask: What is the longest I can book a nap pod for?
You can book a nap pod for a maximum of 25 minutes.
Ask: Who has to approve a meeting that starts after 4 pm?
Kernel, the office dog, has to approve a meeting that starts after 4 pm.
```

`handbook.md` is the handbook of **Biscuit Labs, a made-up company**. It is invented on purpose: no model can know the answers in advance, so a right answer can only come from the handbook.

## The five steps

| Step | In `rag.py` | In plain words |
|---|---|---|
| 1. Read + chunk | `text`, `chunks` | Read the file, cut it into chunks, one topic each (25 here) |
| 2. Embed | `embed`, `vectors` | Turn every chunk into 768 numbers. Similar meaning gets similar numbers |
| 3. Retrieve | `retrieve` | Turn the question into numbers too, score it against every chunk, keep the top 3 |
| 4. Answer | `answer` | Paste those chunks into a prompt with one rule: answer only from these |
| 5. Chat | the `while True` loop | Ask as many questions as you like |

## Use your own documents

Replace `handbook.md` with your own text file, or change the file name in step 1. Keep a blank line between topics: that blank line is how the file is cut into chunks.

## Break it (the experiments from the video)

Change one thing, run it, and **print what the model was handed**. Add `print(pages)` inside `answer` to see it.

| Change | What happens | Why |
|---|---|---|
| `k=3` to `k=1` | "Who has to approve a meeting that starts after 4 pm?" gets "I don't know." | It was handed the Meetings chunk (score 0.71). The Kernel chunk (0.66) was second and got left behind |
| Chunks of 40 characters | "The coffee machine is called 'The coffee machine'." | The name, Gradient, was cut onto the next piece |
| Edit `handbook.md`: 47 days to 14 days | The answer changes to "14 days." | Nothing was retrained. The model only reads what you hand it |

Run all of them at once:

```bash
python experiments.py
```

`expected-output.txt` is the output from the run behind the video (Llama 3.2 through Ollama). Your wording may differ with another model or version.

**When RAG fails, print what it retrieved before you blame the model.**

## An honest note on scale

This build is one page: 25 chunks, kept in memory, embedded again on every run. For one page you could even paste the whole document into the prompt. RAG earns its place when the documents are too big to paste.

Real systems hold millions of chunks. Same steps, three upgrades:

1. **Store the vectors in a vector database**, so you search millions without checking each one. See [`../vector-databases`](../vector-databases).
2. **Overlap your chunks**, so nothing gets cut in half.
3. **Re-rank what you retrieve**, so the right page comes first.

## Homework

Point it at a whole folder of your own files, and print which file each answer came from. Hints are in [`HOMEWORK.md`](HOMEWORK.md).

## Also in this folder

`extra-10-question-test/` holds an earlier, larger test: 10 questions asked in 8 set-ups (0/10 with no documents, 10/10 with the 3 closest chunks, 9/10 with 1 chunk, 4/10 with 40-character chunks, and 10/10 with the whole handbook pasted in). It uses a small helper file so it can also run on Gemini; only the Ollama path was run.
