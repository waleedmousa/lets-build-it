import ollama
import numpy as np

# 1. READ the document, cut it into chunks
text = open("handbook.md", encoding="utf-8").read()
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

# 2. EMBED: turn text into numbers
def embed(texts):
    r = ollama.embed(model="nomic-embed-text", input=texts)
    v = np.array(r["embeddings"])
    return v / np.linalg.norm(v, axis=1, keepdims=True)

vectors = embed(chunks)

# 3. RETRIEVE: the chunks closest to the question
def retrieve(question, k=3):
    scores = vectors @ embed([question])[0]
    best = scores.argsort()[::-1][:k]
    return [chunks[i] for i in best]

# 4. ANSWER: paste those chunks into the prompt, then ask
def answer(question, k=3):
    pages = "\n\n".join(retrieve(question, k))
    prompt = f"""Answer using only the handbook pages below.
If the answer is not there, say "I don't know".
Answer in one short sentence.

{pages}

Question: {question}"""
    reply = ollama.chat(model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0})
    return reply["message"]["content"]

# 5. CHAT with your document
while True:
    print(answer(input("Ask: ")))
