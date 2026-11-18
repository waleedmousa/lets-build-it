# Snake that teaches itself (EP 13)

An AI that has never played Snake learns to play it in about two seconds. No libraries, no examples, nobody tells it the rules. Its whole "brain" is a table of 669 numbers.

The technique is called **Q-learning**: play, get a score, nudge a number. That's all.

| File | What it is | Average score after training |
|---|---|---|
| `snake_ai.py` | The version built in the video, about 50 lines of code | **17.6** |
| `snake_ai_v2.py` | Same file plus one new sense: "is that way a dead end?" | **30.9** |

## Run it

You need Python 3. Nothing to install.

```
mkdir snake-ai && cd snake-ai
# save snake_ai.py here
python snake_ai.py
```

You should see exactly this (the random seed is fixed, so your numbers will match):

```
game 500: average score 0.8
game 1000: average score 4.9
game 1500: average score 16.8
game 2000: average score 17.4
game 2500: average score 17.2
game 3000: average score 17.6
```

Each line is the average score over the last 500 practice games. It took about 2 seconds on our machine; yours may be faster or slower.

## The five parts

1. **The game.** A 10 x 10 board, a snake, one piece of food. Hit a wall or yourself and the game ends.
2. **What it sees.** Not the screen. Eight small facts: is there danger to the left, ahead, or right; is the food left, right, up, or down; and which way it is heading.
3. **Its memory.** A dictionary, `Q`. For every situation and each of the three moves (turn left, go straight, turn right) it holds one number: how well did this go before? It starts empty.
4. **Play and learn.** Pick the move with the best number. Eating food is worth +10, crashing is -10. Then move that number a little toward what really happened:
   `Q[(state, turn)] = old + 0.1 * (reward + 0.9 * future - old)`
5. **Practice.** 3,000 games. Early on most moves are random, and that share drops to zero by game 1,000, because you can't learn from moves you never try.

## Break it (both are in the video)

**1. Take away the food reward.** In `play`, change the `10` to `0`:

```python
reward, score, hungry = 0, score + 1, 0      # food
```

Train again. Every average is `0.0`. It did learn something, exactly what you still pay for: don't die. So it circles in a tiny loop until the game cuts it off.

**2. Switch off the random moves.** Put the 10 back, then change the practice line:

```python
total += play(explore=0.0)
```

`0.0` again. It never tries anything new, so it never discovers that food is good.

## The honest limit

`snake_ai.py` only sees one step ahead. In 200 test games after training, 183 ended with the snake running into its own body, usually after walking into a pocket it couldn't get out of.

`snake_ai_v2.py` changes one thing: instead of "is the next square blocked?", it asks "is that way a dead end?", by counting how many squares it could still reach from there. Same learning, same rewards, same 3,000 games. The average goes from 17.6 to 30.9.

This is a 10 x 10 board and a table. The systems that play Atari or Go run the same loop (play, score, nudge), but they replace the table with a neural network, because their games have far too many situations to list.

## Homework: beat 30

Give it a better sense, train it, and post your score. Some places to start:

- Let it see how long it is.
- Tell it how far away the food is, not just the direction.
- Change the rewards, the 3,000 games, or how fast the random moves fade.
- Make the board bigger (`SIZE = 20`) and see what breaks.

One warning from our own tests: we first tried "see two steps ahead" and the score got *worse* (about 12). More information is not always better; the table gets bigger and each number gets less practice.
