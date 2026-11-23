# 100 birds that learn to fly (EP 14)

One hundred birds with random brains play a tap-to-fly game. In generation one, every bird crashes before the first pipe is behind it. Ten generations later, one of them flies through 1,000 pipes.

Nobody teaches them. There is no training data and no reward table. The best birds get to have children, and the children are slightly different. That's all. The technique is called **neuroevolution**: a tiny neural network, trained by evolution.

It sounds hard. It is about 60 lines of plain Python.

| File | What it is | Result | Time |
|---|---|---|---|
| `birds.py` | The version built in the video | A bird passes 1,000 pipes in generation 10 | about 2 seconds |
| `birds_v2.py` | Same file, but it keeps evolving for 30 generations and then takes an exam | Perfect on 30 of 30 new courses | 1 to 2 minutes |

## Run it

You need Python 3. Nothing to install.

```
mkdir birds && cd birds
# save birds.py here
python birds.py
```

You should see exactly this (the random seed is fixed, so your numbers will match):

```
generation 1: best bird passed 0
generation 2: best bird passed 1
generation 3: best bird passed 4
generation 4: best bird passed 2
generation 5: best bird passed 18
generation 6: best bird passed 373
generation 7: best bird passed 130
generation 8: best bird passed 200
generation 9: best bird passed 206
generation 10: best bird passed 1000
```

The number is how many pipes the best bird of that generation passed. The run stops when a bird reaches 1,000.

On Windows the command may be `py birds.py`; on Mac or Linux it may be `python3 birds.py`.

**Why does the score sometimes go down (373, then 130)?** Every generation flies a brand-new random course. Some courses are harder than others.

## The five parts

1. **The game.** Pipes slide in from the right, each with a gap at a random height. Gravity pulls the bird down. A flap pushes it up. Touch a pipe, the floor or the ceiling and the bird is out.
2. **The brain.** A list of 25 random numbers. That is the whole neural network. Four facts go in (my height, the gap's height, my speed, the distance to the pipe). The numbers multiply and add them up, and one answer comes out: flap, or don't.
3. **One generation.** One round. All 100 birds fly the same course and we record how many frames each one lasted.
4. **Evolution.** One line: copy a winner and change every number a little.
   `return [w + random.gauss(0, 0.3) for w in parent]`
5. **Repeat.** Keep the best 10 unchanged. Fill the other 90 seats with their children. Go again.

Generation one, by the way: 50 birds flap non-stop into the ceiling, 46 never flap and hit the floor, and 4 reach the first pipe and crash into it.

## Break it (both are in the video)

**1. Take away the nudge.** In `child`, change `0.3` to `0.0`, so children are perfect copies:

```python
return [w + random.gauss(0, 0.0) for w in parent]
```

Nothing new is ever tried, so nothing improves. In the first 40 generations the best any bird does is 9 pipes. The file keeps going to generation 100 (about 15 seconds); the best over all 100 is 14.

**2. Pick the parents at random.** Put `0.3` back, then replace the `order = ...` line:

```python
order = random.sample(range(BIRDS), BIRDS)
```

Now there are changes but no filter. In the first 40 generations the best is 8 pipes. In generation 41 one lucky bird passes 27, its luck is not kept, and the rest of the run is zeros.

Evolution needs both: small changes, and a filter.

## The honest limit, and the fix

The champion from `birds.py` passed 1,000 pipes, but on one course. `birds_v2.py` adds an exam: the champion flies alone on 30 courses it has never seen.

- Stop after 10 generations (set `GENERATIONS = 10`): `exam: perfect on 5 of 30 new courses`. It was good, and a little lucky.
- Keep evolving for 30 generations (the default): `exam: perfect on 30 of 30 new courses`.

`birds_v2.py` takes 1 to 2 minutes, because once the birds are good, 100 of them each fly 1,000 pipes every generation. It prints a line per generation, so you can see it working. The full output is in `expected-output.txt`.

## How this compares to the real thing

Same loop, different size. In 2017, researchers at Uber AI Labs used a simple genetic algorithm to evolve networks with over four million numbers that play Atari games ([Such et al., "Deep Neuroevolution"](https://arxiv.org/abs/1712.06567)). Ours has 25.

Most neural networks today are trained a different way (gradient descent), which is far more efficient for big models. Evolution is the simplest way to see a network learn with nothing but trial, error and selection.

## Homework: shrink the gap

At the top of `birds.py`, change the gap from `0.30` to `0.20`:

```python
GAP, BIRD_X = 0.20, 0.2
```

How many generations does your flock need now? (With the seed in the file, ours needed 20.) Then try:

- Change `random.seed(3)` to another number. Across 20 seeds we tried, the normal game took between 4 and 18 generations.
- Change the nudge from `0.3` to `0.05` or `1.0`. Too small and too big both hurt. Why?
- Keep the best 2 instead of the best 10 (`KEEP`), and change the `90` to `98`.
- Remove one of the four facts the bird sees. Which one can it live without?

## What we tested before publishing

- Both files were downloaded fresh from this repo and run on Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 and 3.14. All seven printed exactly the expected output.
- Both "break it" edits and the homework edit were applied exactly as written and gave the results stated above.
- The files use only Python's built-in `math` and `random` modules.
- Tested on Linux. Nothing in the code is system-specific, but we have not run it on Windows or macOS ourselves.
