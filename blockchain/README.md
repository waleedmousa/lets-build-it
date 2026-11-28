# Let's Build It 17 · A blockchain you can try to rob

A working chain of blocks in 39 lines of Python. No installs.

## Run it

```bash
python chain.py
```

You should see (the last time will differ on your computer):

```
0 0000a3119697eead lucky=12994   start
1 0000dcde053ab879 lucky=24675   Ali pays Sara 10
2 0000addb1c608382 lucky=71744   Sara pays Omar 4
3 0000113ba0ede9b8 lucky=41881   Omar pays Ali 7
4 00001cb75cedc001 lucky=27598   Ali pays Omar 2
check: all good
after the cheat: BROKEN: block 1 was changed
after re-mining block 1: BROKEN: block 2 does not link to block 1
after re-mining everything: all good (0.05 s of work)
```

## What is in it

| Piece | In the code | What it does |
|---|---|---|
| Fingerprint | `fingerprint()` | SHA-256 of the block's contents: 64 characters. Change one letter and it all changes. |
| Mining | `mine()` | Tries lucky numbers until the fingerprint starts with `ZEROS` zeros. |
| The chain | `add()` | Every new block stores the fingerprint of the block before it. |
| The check | `check()` | Recomputes every fingerprint, demands the required zeros (proof of work), and follows the links. |

Then the script cheats three times: it changes an old payment, re-mines that one
block, and finally re-mines every block after it.

## Feel your laptop sweat

Change `ZEROS = 4` near the top and run it again. Each extra zero is 16 times
more work on average. Building the 5-block chain on my machine took:

| ZEROS | Time |
|---|---|
| 4 | 0.12 s |
| 5 | 1.5 s |
| 6 | 82 s |
| 7 | 10 min 20 s |

Your times will differ, and luck matters: sometimes a block is found early.
6 already takes a minute or more; 7 is a coffee break.

## Honest notes

- This is the chain itself. Real blockchains add two big things: a network of
  thousands of computers that each hold a copy and agree on the valid chain with the
  most accumulated proof of work,
  and digital signatures that prove who is allowed to spend.
- "Starts with N zeros" is a simplification of how Bitcoin states its target, but
  it is the same idea. A recent Bitcoin block (976,124) has a fingerprint that
  starts with 19 zeros.
- "Over a billion years on my laptop" in the video is my own estimate: 16^19
  tries at about 1.8 million tries per second, for one block.
- The check refuses a block whose fingerprint does not start with the required zeros,
  so a cheater cannot just recompute fingerprints and relink the chain. Every
  rewritten block has to be mined again.
- On this tiny chain the full cheat takes a fraction of a second. That is the
  point of the mining section: security comes from making that work expensive.

Video: Runtime Explained on YouTube, playlist "Let's Build It".
