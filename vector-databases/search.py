import chromadb
from wordllama import WordLlama

tickets = [
    "Password reset link not working",
    "Charged twice for my subscription",
    "App crashes when I upload a photo",
    "How do I change my delivery address?",
    "Refund still not received after 10 days",
    "Cannot find the invoice for last month",
    "Notifications arrive hours late",
    "Promo code says it is expired",
]

# 1. text -> 256 numbers
model = WordLlama.load()
vectors = model.embed(tickets)

# 2. store them in Chroma
db = chromadb.Client().create_collection(
    "tickets", metadata={"hnsw:space": "cosine"})
ids = [str(i) for i in range(len(tickets))]
db.add(ids=ids, documents=tickets, embeddings=vectors)

# 3. ask by meaning
question = "I can't log in"
hit = db.query(
    query_embeddings=model.embed([question]),
    n_results=1)
print(hit["documents"][0][0])
print(round(hit["distances"][0][0], 2))
