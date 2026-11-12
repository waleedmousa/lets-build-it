"""The two things we borrow from a real model: embed() and ask().

Works with Gemini (set GEMINI_API_KEY) or with Ollama running on your machine.
Pick one with RAG_BACKEND=gemini or RAG_BACKEND=ollama. Default: Gemini if a key
is set, otherwise Ollama.
"""
import os, re, json, time, hashlib, urllib.request
import numpy as np

BACKEND = os.environ.get("RAG_BACKEND") or ("gemini" if os.environ.get("GEMINI_API_KEY") else "ollama")
PAUSE = float(os.environ.get("RAG_PAUSE", "4" if BACKEND == "gemini" else "0"))  # seconds between calls
CACHE_FILE = "cache.json"
_cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {}

def _retry(fn):
    for attempt in range(6):
        try:
            return fn()
        except Exception as e:                       # rate limit or a network blip: wait, try again
            if attempt == 5: raise
            wait = 15 * (attempt + 1)
            print(f"   ({type(e).__name__}: waiting {wait}s, then trying again)")
            time.sleep(wait)

if BACKEND == "gemini":
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    def _pick(pattern, action, override):
        if os.environ.get(override): return os.environ[override]
        names = [m.name.split("/")[-1] for m in client.models.list() if action in (m.supported_actions or [])]
        good = sorted((n for n in names if re.fullmatch(pattern, n)),
                      key=lambda n: [float(x) for x in re.findall(r"\d+(?:\.\d+)?", n)] or [0])
        if not good: raise SystemExit(f"No model matched. Set {override} to one of: {names}")
        return good[-1]
    CHAT_MODEL = _pick(r"gemini-[\d.]+-flash", "generateContent", "RAG_CHAT_MODEL")
    EMBED_MODEL = _pick(r"gemini-embedding-[\d.]+|text-embedding-[\d.]+", "embedContent", "RAG_EMBED_MODEL")
    def _embed(texts):
        out = []
        for i in range(0, len(texts), 50):
            r = _retry(lambda: client.models.embed_content(model=EMBED_MODEL, contents=texts[i:i + 50]))
            out += [e.values for e in r.embeddings]; time.sleep(PAUSE)
        return out
    def _ask(prompt):
        r = _retry(lambda: client.models.generate_content(model=CHAT_MODEL, contents=prompt, config={"temperature": 0}))
        time.sleep(PAUSE); return (r.text or "").strip()
else:
    HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    CHAT_MODEL = os.environ.get("RAG_CHAT_MODEL", "llama3.2")
    EMBED_MODEL = os.environ.get("RAG_EMBED_MODEL", "nomic-embed-text")
    def _post(path, body):
        req = urllib.request.Request(HOST + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=600))
    def _embed(texts):
        return _retry(lambda: _post("/api/embed", {"model": EMBED_MODEL, "input": texts}))["embeddings"]
    def _ask(prompt):
        r = _retry(lambda: _post("/api/chat", {"model": CHAT_MODEL, "stream": False, "options": {"temperature": 0},
                                               "messages": [{"role": "user", "content": prompt}]}))
        return r["message"]["content"].strip()

def embed(texts):
    """Turn a list of texts into a table of numbers, one row per text, each row of length 1."""
    v = np.array(_embed(list(texts)), dtype=float)
    return v / np.linalg.norm(v, axis=1, keepdims=True)

def ask(prompt):
    """Send a prompt to the model, get its reply. Replies are cached so a re-run costs nothing."""
    key = hashlib.sha1((CHAT_MODEL + "\n" + prompt).encode()).hexdigest()
    if key not in _cache:
        _cache[key] = _ask(prompt)
        json.dump(_cache, open(CACHE_FILE, "w"))
    return _cache[key]
