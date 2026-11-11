# Build a tiny LLM from scratch, then break it

The code from the Runtime Explained short **"This AI Has Never Read a Word. Give It 1 Minute."** (Let's Build It, EP 10).

Every LLM, tiny or giant, is five blocks: data, tokens, a model, a way to write, and training. This folder builds all five in about 70 lines. No API key, no downloaded model, no dataset to fetch.

## Run it

You need Python 3.9 or newer.

```bash
pip install torch
python tiny_llm.py
```

Training takes about a minute on a 2-core CPU. This is what my run printed:

```
454780 letters: the assert statement
29 tokens: tensor([22, 10,  7,  0])
345725 dials
untrained: the wehtficowtgqtlecuayiw titzpcov ,ktdhd sho cjhyvzr,wgrcgepgariifgprgasi
0 3.69 the e o ae stao  e    y f rt  a  r   l t a e  r     p re  r r g e   vr a
500 1.46 the using the clocate is sided to on the code only the filluation the are
1000 1.24 the eputatoms are class to the st is class that is not string not operatio
1500 1.23 the using treated, .  should corvalue are and complex booleans execution m
2000 1.15 the class parameter are used follows to reflections, class for the call cu
'python is ' -> python is an equivalent class immediately is that olted to b
'if you ' -> if you compare rest class implement is that has name many
```

Each training line shows the round, the score (lower is better) and a sample of its writing. The full output is in `expected-output.txt`.

**Your text will differ.** Different Python and PyTorch versions give different samples, and the manual itself changes between Python versions. The pattern is what matters: random letters first, then near-English.

## The five blocks

| Block | In the code | In plain words |
|---|---|---|
| 1. Data | `text = ...` | Something to read. Here: Python's own manual, which ships with Python. |
| 2. Tokens | `chars`, `data` | A model reads numbers, not letters. We list our 29 characters and swap each letter for its number. |
| 3. Model | `class TinyLLM` | Takes tokens in, gives a score to every token for what comes next. 345,725 dials (parameters). |
| 4. Writing | `def write(...)` | Guess a letter, add it, guess again. |
| 5. Training | the `for step in range(2001)` loop | Guess the next letter, measure how wrong it was, nudge every dial. 2,000 times. |

## Break it: the two experiments from the video

`experiments.py` trains a model, writes one page of text, and scores how much of the page is **real words**: the share of letters that sit inside a word (2+ letters) found somewhere in the training text. It is a rough score for "does this look like the book". It does not measure understanding.

```bash
python experiments.py tiny_llm.py              # the full model
python experiments.py step5_simple_model.py    # the transformer block removed
```

My runs:

| | Real words |
|---|---|
| Before training | 1% |
| Trained (temperature 0.8) | 89% |
| **Experiment 1:** transformer block removed, trained the same way | 9% |
| **Experiment 2:** temperature 0.2 | 99% (and very repetitive) |
| **Experiment 2:** temperature 2.0 | 10% |

**Experiment 1.** `step5_simple_model.py` is the same file without the 10 transformer lines in the model. That model sees only one letter at a time, so it can only guess from a single letter. It trains in about 5 seconds and writes word shapes, not words:

```
2000 2.36 the alis en faname f an th me tse ith  alle ale oras th teromononectome ur
```

| | Block removed | With the transformer block |
|---|---|---|
| What it sees | The last letter | The last 48 letters |
| Dials | 5,597 | 345,725 |
| Training time | about 5 s | about 68 s |
| Final score (lower is better) | 2.36 | 1.15 |
| Real words | 9% | 89% |

**Experiment 2.** Temperature is the `temperature=0.8` in `write(...)`. Low values make it pick its top guess almost every time (safe, repetitive). High values flatten the odds (creative, then chaos). Nothing is retrained; it is the same model writing differently.

## Where to take it

The five blocks stay the same. You change what goes into them.

- **Your LinkedIn posts** → a post planner that drafts in your voice.
- **Your support tickets** → a first-draft reply writer.
- **Your team's docs** → an assistant that writes like your docs.

For results you would use, start from a pretrained model and fine-tune it on your text: that is the same five blocks with a much bigger brain. This file is for understanding how it works. To try your own text here:

- **Your own text.** Replace the first `text = ...` line with `text = open("my_notes.txt", encoding="utf-8").read().lower()`. Use a few hundred thousand characters or more.
- **Train longer.** Raise `range(2001)`.
- **Stack more blocks.** Change the `3` in `nn.TransformerEncoder(block, 3, ...)`.
- **Look further back.** Raise `CTX`.
- **Whole words instead of letters.** Change the Tokens block so each token is a word or a piece of a word.

## Good to know

- **Tested with** Python 3.13 and torch 2.15.0, on CPU.
- **It learns letters, not facts.** After a minute on one manual it writes text that looks like the manual. It does not understand Python.
- **Real LLMs use the same five blocks at a different scale:** far more text, tokens that are pieces of words, and billions of dials.
