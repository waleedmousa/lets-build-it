"""Runs every experiment for the video and saves the results to results.json.

    python run_experiments.py

It asks the same 10 questions in several set-ups and marks each reply:
  right        the reply contains the fact from the handbook
  dont_know    the reply says it does not know
  wrong        anything else (a confident guess)
The marking is automatic and rough (it looks for key words), so read the replies too.
Replies are cached in cache.json, so if it stops half way, just run it again.
"""
import json, re, time, platform
import numpy as np
import llm
from llm import embed, ask

t0 = time.time()
text = open("handbook.md", encoding="utf-8").read()
questions = json.load(open("questions.json", encoding="utf-8"))
print(f"Model: {llm.CHAT_MODEL}   Embeddings: {llm.EMBED_MODEL}   ({llm.BACKEND})")

STRICT = 'Answer using only the handbook pages below.\nIf the answer is not there, say "I don\'t know".\nAnswer in one short sentence.'
LOOSE = "Here are some handbook pages. Answer the question in one short sentence."
CLOSED = "A question about the company Biscuit Labs. {q}\nAnswer in one short sentence."
IDK = ["don't know", "do not know", "not sure", "no information", "don't have", "do not have", "cannot", "can't",
       "unable", "not mentioned", "no mention", "not specified", "not provided", "does not say", "doesn't say",
       "not available", "unknown", "couldn't find", "could not find", "not aware"]

def mark(reply, accept):
    low = reply.lower()
    if any(re.search(r"(?<![\w.])" + re.escape(a) + r"(?![\w])", low) for a in accept): return "right"
    return "dont_know" if any(p in low for p in IDK) else "wrong"

def paragraphs(t): return [c.strip() for c in t.split("\n\n") if c.strip()]
def slices(t, n):
    flat = " ".join(t.split()); return [flat[i:i + n] for i in range(0, len(flat), n)]

q_vecs = embed([q["q"] for q in questions])

def run(name, note, chunks=None, k=3, rule=STRICT, pick="best", vectors=None):
    print(f"\n== {name}: {note}")
    if chunks is not None and vectors is None: vectors = embed(chunks)
    rows = []
    for q, qv in zip(questions, q_vecs):
        if chunks is None:
            prompt, used, scores = CLOSED.format(q=q["q"]), [], []
        else:
            s = vectors @ qv
            order = s.argsort()[::-1] if pick == "best" else s.argsort()
            used = [int(i) for i in order[:k]]; scores = [round(float(s[i]), 4) for i in used]
            prompt = rule + "\n\n" + "\n\n".join(chunks[i] for i in used) + "\n\nQuestion: " + q["q"]
        reply = ask(prompt); m = mark(reply, q["accept"])
        rows.append({"q": q["q"], "reply": reply, "mark": m, "used": used, "scores": scores, "prompt_chars": len(prompt)})
        print(f"   [{m:9s}] {q['q'][:46]:46s} -> {reply[:70]!r}")
    score = sum(r["mark"] == "right" for r in rows)
    print(f"   {score}/10 right, {sum(r['mark']=='dont_know' for r in rows)} don't know, {sum(r['mark']=='wrong' for r in rows)} wrong")
    return {"name": name, "note": note, "k": k, "chunks": chunks, "right": score, "rows": rows}

paras = paragraphs(text); para_vecs = embed(paras)
out = {"backend": llm.BACKEND, "chat_model": llm.CHAT_MODEL, "embed_model": llm.EMBED_MODEL,
       "python": platform.python_version(), "handbook_chars": len(text), "runs": []}
R = out["runs"]
R.append(run("closed_book", "no handbook at all"))
R.append(run("open_book", "one topic per chunk, top 3", paras, 3, vectors=para_vecs))
R.append(run("top_1", "one topic per chunk, top 1 only", paras, 1, vectors=para_vecs))
R.append(run("wrong_pages_strict", "the 3 LEAST similar chunks, with the 'say I don't know' rule", paras, 3, STRICT, "worst", para_vecs))
R.append(run("wrong_pages_loose", "the 3 LEAST similar chunks, without that rule", paras, 3, LOOSE, "worst", para_vecs))
R.append(run("tiny_chunks", "chunks of 40 characters, cut anywhere, top 3", slices(text, 40), 3))
R.append(run("huge_chunks", "the handbook cut into 3 giant chunks, top 1", slices(text, len(" ".join(text.split())) // 3 + 1), 1))
R.append(run("whole_book", "no retrieval: the whole handbook pasted in", [text], 1))

# The update test: change one line of the handbook. No training. Ask again.
new_text = text.replace("within 47 days", "within 14 days"); assert new_text != text
new_paras = paragraphs(new_text); q = questions[0]
used = [int(i) for i in (embed(new_paras) @ q_vecs[0]).argsort()[::-1][:3]]
reply = ask(STRICT + "\n\n" + "\n\n".join(new_paras[i] for i in used) + "\n\nQuestion: " + q["q"])
out["update_test"] = {"q": q["q"], "changed": "47 days -> 14 days", "reply": reply, "mark": mark(reply, ["14"])}
print(f"\n== update_test: handbook now says 14 days -> {reply!r}")

# A flat map of the chunks and questions, for the picture in the video
allv = np.vstack([para_vecs, q_vecs]); c = allv - allv.mean(0)
xy = c @ np.linalg.svd(c, full_matrices=False)[2][:2].T
out["map"] = {"chunks": [[round(float(a), 4) for a in p] for p in xy[:len(paras)]],
              "questions": [[round(float(a), 4) for a in p] for p in xy[len(paras):]]}
out["similarity"] = [[round(float(x), 4) for x in row] for row in (para_vecs @ q_vecs.T).T]
out["seconds"] = round(time.time() - t0, 1)
json.dump(out, open("results.json", "w"), indent=1)
print(f"\nSaved results.json ({out['seconds']}s). Send that file back.")
