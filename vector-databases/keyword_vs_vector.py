"""Break it, then fix it: the same four questions asked two ways.

Keyword search finds nothing. The vector database finds the right ticket every time.
"""
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

questions = [
    "I can't log in",
    "money taken from my card two times",
    "where is my money back?",
    "the app keeps closing",
]

model = WordLlama.load()
db = chromadb.Client().create_collection(
    "tickets", metadata={"hnsw:space": "cosine"})
ids = [str(i) for i in range(len(tickets))]
db.add(ids=ids, documents=tickets, embeddings=model.embed(tickets))


def keyword_search(question):
    """A ticket matches only if it contains every word of the question."""
    words = question.lower().replace("'", "").replace("?", "").split()
    return [t for t in tickets if all(w in t.lower() for w in words)]


for question in questions:
    hit = db.query(query_embeddings=model.embed([question]), n_results=3)
    print(f"\nQ: {question}")
    print(f"  keyword search: {keyword_search(question)}")
    print("  vector search:")
    for doc, dist in zip(hit["documents"][0], hit["distances"][0]):
        print(f"    {dist:.2f}  {doc}")
