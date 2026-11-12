"""The "break it" experiments from the video, in one run.

    python experiments.py

It loads rag.py (everything above "# 5. CHAT"), then:
  1. asks two questions the normal way
  2. asks again with k = 1 and prints what the model was handed
  3. cuts the chunks to 40 characters and asks about the coffee machine
  4. changes one line of the handbook (47 days -> 14 days) and asks again
"""
import ollama

g = {}
exec(open("rag.py", encoding="utf-8").read().split("# 5. CHAT")[0], g)
answer, retrieve, embed = g["answer"], g["retrieve"], g["embed"]

Q_NAP = "What is the longest I can book a nap pod for?"
Q_MEET = "Who has to approve a meeting that starts after 4 pm?"
Q_COFFEE = "What is the coffee machine called?"
Q_REFUND = "How many days does a customer have to ask for a refund?"

print("NO DOCUMENTS")
r = ollama.chat(model="llama3.2", options={"temperature": 0}, messages=[{"role": "user",
    "content": "A question about the company Biscuit Labs. " + Q_NAP + "\nAnswer in one short sentence."}])
print("  ", r["message"]["content"])

print("\nRAG, 3 chunks")
print("   chunks:", len(g["chunks"]), "  vectors:", g["vectors"].shape)
for q in (Q_NAP, Q_MEET):
    print("  ", q, "->", answer(q))

print("\nBREAK 1: k = 1")
print("   handed:", retrieve(Q_MEET, 1)[0].split("\n")[0])
print("  ", Q_MEET, "->", answer(Q_MEET, 1))

print("\nBREAK 2: chunks of 40 characters")
keep = (g["chunks"], g["vectors"])
flat = " ".join(g["text"].split())
g["chunks"] = [flat[i:i + 40] for i in range(0, len(flat), 40)]
g["vectors"] = embed(g["chunks"])
print("   handed:", retrieve(Q_COFFEE))
print("  ", Q_COFFEE, "->", answer(Q_COFFEE))
g["chunks"], g["vectors"] = keep

print("\nEDIT THE DOCUMENT: 47 days becomes 14 days, no retraining")
print("   before:", answer(Q_REFUND))
new = g["text"].replace("within 47 days", "within 14 days")
g["chunks"] = [c.strip() for c in new.split("\n\n") if c.strip()]
g["vectors"] = embed(g["chunks"])
print("   after: ", answer(Q_REFUND))
