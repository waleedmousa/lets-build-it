import torch, torch.nn as nn
import pydoc_data.topics as docs

# 1. DATA: Python's own manual, already on your laptop
text = " ".join(docs.topics.values()).lower()
text = " ".join(text.split())
keep = "abcdefghijklmnopqrstuvwxyz .,"
text = "".join(c for c in text if c in keep)
print(len(text), "letters:", text[:20])

# 2. TOKENS: every letter becomes a number
chars = sorted(set(text))
data = torch.tensor([chars.index(c) for c in text])
print(len(chars), "tokens:", data[:4])

# 3. MODEL: score every token for what comes next
CTX, DIM = 48, 96
no_peeking = nn.Transformer.generate_square_subsequent_mask

class TinyLLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(len(chars), DIM)
        self.pos = nn.Embedding(CTX, DIM)
        block = nn.TransformerEncoderLayer(
            DIM, 4, DIM * 4, dropout=0.0,
            batch_first=True, norm_first=True)
        self.blocks = nn.TransformerEncoder(
            block, 3, enable_nested_tensor=False)
        self.out = nn.Linear(DIM, len(chars))

    def forward(self, x):
        h = self.tok(x)
        n = x.shape[1]
        h = h + self.pos(torch.arange(n))
        h = self.blocks(h, mask=no_peeking(n))
        return self.out(h)

torch.manual_seed(0)
model = TinyLLM()
print(sum(p.numel() for p in model.parameters()), "dials")

# 4. WRITING: guess a letter, add it, guess again
@torch.no_grad()
def write(start="the ", n=70, temperature=0.8):
    ids = [chars.index(c) for c in start]
    for _ in range(n):
        scores = model(torch.tensor([ids[-CTX:]]))[0, -1]
        probs = torch.softmax(scores / temperature, 0)
        ids.append(torch.multinomial(probs, 1).item())
    return "".join(chars[i] for i in ids)

print("untrained:", write())

# 5. TRAINING: guess, measure how wrong, nudge every dial
opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
for step in range(2001):
    i = torch.randint(len(data) - CTX - 1, (32,))
    x = torch.stack([data[j:j + CTX] for j in i])
    y = torch.stack([data[j + 1:j + CTX + 1] for j in i])
    loss = nn.functional.cross_entropy(
        model(x).flatten(0, 1), y.flatten())
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 500 == 0:
        print(step, round(loss.item(), 2), write())

# TEST IT
prompts = ["python is ", "a function ",
           "the error ", "if you "]
for p in prompts:
    print(repr(p), "->", write(p, 50))
