"""The two experiments from the video, plus the "real words" score.

    python experiments.py tiny_llm.py              # the full model
    python experiments.py step5_simple_model.py    # the transformer block removed

It trains the model from the file you name, then writes one page at three
temperatures and prints how much of each page is real words.

"Real words" = the share of letters that sit inside a word (2+ letters)
that appears somewhere in the training text. It is a rough score for
"does this look like the book", not a measure of understanding.
"""
import sys, io, contextlib, re, torch, torch.nn as nn

fn = sys.argv[1] if len(sys.argv) > 1 else "tiny_llm.py"
head = open(fn).read().split("# 5. TRAINING")[0]      # blocks 1 to 4, unchanged
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(head, g)
model, data, chars, CTX, text = g["model"], g["data"], g["chars"], g["CTX"], g["text"]
vocab = set(w for w in re.findall(r"[a-z]+", text) if len(w) >= 2)

@torch.no_grad()
def page(temperature=0.8, n=396):
    state = torch.get_rng_state(); torch.manual_seed(7)   # same dice for every page
    ids = [chars.index(c) for c in "the "]
    for _ in range(n):
        p = torch.softmax(model(torch.tensor([ids[-CTX:]]))[0, -1] / temperature, 0)
        ids.append(torch.multinomial(p, 1).item())
    torch.set_rng_state(state)
    return "".join(chars[i] for i in ids)[:396]

def real_words(s):
    words = re.findall(r"[a-z]+", s)
    return round(100 * sum(len(w) for w in words if w in vocab) / max(1, sum(len(w) for w in words)))

print(f"{fn}  before training: {real_words(page())}% real words")

# block 5, the same loop as in the file
opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
for step in range(2001):
    i = torch.randint(len(data) - CTX - 1, (32,))
    x = torch.stack([data[j:j + CTX] for j in i])
    y = torch.stack([data[j + 1:j + CTX + 1] for j in i])
    loss = nn.functional.cross_entropy(model(x).flatten(0, 1), y.flatten())
    opt.zero_grad(); loss.backward(); opt.step()

for t in (0.2, 0.8, 2.0):
    s = page(t)
    print(f"temperature {t}: {real_words(s):3d}% real words | {s[:60]}")
