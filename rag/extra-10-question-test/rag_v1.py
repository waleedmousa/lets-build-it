import sys
from llm import embed, ask

# 1. DOCUMENTS: the book the model has never read
text = open("handbook.md", encoding="utf-8").read()

# 2. CHUNKS: cut it into small pieces, one topic each
chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

# 3. EMBEDDINGS: turn every piece into numbers
vectors = embed(chunks)

# 4. RETRIEVE: find the pieces closest to the question
def retrieve(question, k=3):
    scores = vectors @ embed([question])[0]
    best = scores.argsort()[::-1][:k]
    return [chunks[i] for i in best]

# 5. ANSWER: hand the model those pieces, then ask
def answer(question, k=3):
    pages = "\n\n".join(retrieve(question, k))
    return ask(f"""Answer using only the handbook pages below.
If the answer is not there, say "I don't know".
Answer in one short sentence.

{pages}

Question: {question}""")

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How many days does a customer have to ask for a refund?"
    print("Closed book:", ask("A question about the company Biscuit Labs. " + question + "\nAnswer in one short sentence."))
    print("Open book:  ", answer(question))
