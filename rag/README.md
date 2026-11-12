# Chat with your own documents: RAG from scratch

The code from the Runtime Explained short **"The New Intern"** (Let's Build It, EP 11).

RAG (retrieval-augmented generation) is an open-book exam. The model does not get smarter. Before it answers, we hand it the right pages.

`rag.py` is the whole thing in about 30 lines and five steps. No framework and no vector database, so nothing is hidden.

| Step | In the code | In plain words |
|---|---|---|
| 1. Documents | `text = open("handbook.md")...` | The book the model has never read |
| 2. Chunks | `chunks = ...` | Cut it into cards, one topic each (25 cards here) |
| 3. Embeddings | `vectors = embed(chunks)` | Turn every card into numbers, so similar cards sit close together |
| 4. Retrieve | `def retrieve(question, k=3)` | Turn the question into numbers too, grab the 3 closest cards |
| 5. Answer | `def answer(question, k=3)` | Hand the model those cards and one rule: answer only from these |

`handbook.md` is the handbook of **Biscuit Labs, a made-up company**. It is invented on purpose: no model can know the answers in advance, so a right answer can only come from the handbook.

## Run it (free, on your own computer)

You need Python 3.9 or newer and [Ollama](https://ollama.com).

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
pip install numpy
RAG_BACKEND=ollama python rag.py "How long can I book a nap pod for?"
```

You get two answers: one with the book closed, one with it open.

**Prefer Gemini?** `pip install -r requirements.txt`, set `GEMINI_API_KEY`, then `python rag.py "your question"`. The Ollama path is the one that was run for the video. The Gemini path was written but not run end to end, so open an issue if it trips.

## Use your own documents

Replace `handbook.md` with your own text file (notes, docs, a policy, a manual) and ask it anything:

```bash
RAG_BACKEND=ollama python rag.py "your question"
```

Keep a blank line between topics. That blank line is how the file is cut into cards.

## Break it: the experiments from the video

```bash
RAG_BACKEND=ollama python run_experiments.py
```

It asks the same 10 questions (`questions.json`) in 8 set-ups. The run behind the video (Llama 3.2 through Ollama, 29 seconds in total):

| Set-up | Right out of 10 | What happened |
|---|---|---|
| Closed book, no handbook | 0 | Nine "I couldn't find Biscuit Labs", one invented answer ("according to their website... 2 hours") |
| **RAG: 3 closest cards** | **10** | Every answer correct |
| Only the 1 closest card | 9 | "Who approves a late meeting?" pulled the Meetings card, not the Kernel card |
| Cards cut to 40 characters | 4 | Facts get cut in half. "The coffee machine is called 'The coffee machine'." |
| The 3 least similar cards | 0 | Ten honest "I don't know"s, nothing invented |
| Handbook cut into 3 giant chunks, 1 used | 7 | The answer is often in a different third |
| The whole handbook pasted in, no retrieval | 10 | Works, because this handbook is one page |
| Change "47 days" to "14 days" in the handbook | answer changes | "14 days." with no retraining |

Every reply from that run is in `expected-output.txt`.

### Read this before you draw conclusions

- **One small model, one small handbook, 10 questions.** These numbers show the idea. They are not a benchmark.
- **Pasting the whole handbook also scored 10/10.** For one page you do not need RAG. You need it when the book is thousands of pages and will not fit, or would cost too much to send every time. Here the RAG prompt was about 6 times shorter than the whole-handbook prompt.
- **The marking is automatic and rough.** It looks for key words in the reply. The table above was checked by reading every reply.
- **Your replies will differ** with another model or version. The pattern is what matters.

## What a real system adds

The same five steps, at scale: a vector database for step 3 and 4 (see [`../vector-databases`](../vector-databases)), smarter chunking, re-ranking the retrieved cards, and showing the source next to every answer.
