import numpy as np

rng = np.random.default_rng(0)

# 1. THE PICTURE: every # becomes a cloud of dots
PICTURE = [
    "...#######...",
    "..#.......#..",
    ".#..#...#..#.",
    ".#..#...#..#.",
    ".#.........#.",
    ".#.#.....#.#.",
    ".#..#####..#.",
    "..#.......#..",
    "...#######...",
]
WIDE, TALL = len(PICTURE[0]), len(PICTURE)
INK = np.array([(x, y) for y, row in enumerate(PICTURE)
                for x, c in enumerate(row) if c == "#"])

def real_dots(n):
    spot = INK[rng.integers(len(INK), size=n)] + rng.random((n, 2))
    return spot / [WIDE, TALL] * 2 - 1

# 2. NOISE: 50 steps from a clean picture to pure static
STEPS = 50
add = np.linspace(0.01, 0.45, STEPS) ** 2
keep = np.cumprod(1 - add)

def make_noisy(dots, step, noise):
    k = keep[step][:, None]
    return np.sqrt(k) * dots + np.sqrt(1 - k) * noise

# 3. THE BRAIN: sees a noisy dot and the step, guesses the noise
def describe(dots, step):
    waves = dots[:, :, None] * np.arange(1, 7) * np.pi
    waves = waves.reshape(len(dots), -1)
    when = step[:, None] / STEPS * np.arange(1, 4) * 2 * np.pi
    return np.hstack([dots, np.sin(waves), np.cos(waves),
                      np.sin(when), np.cos(when)])

SIZES = [32, 128, 128, 2]
brain = []
for a, b in zip(SIZES, SIZES[1:]):
    brain += [rng.normal(0, a ** -0.5, (a, b)), np.zeros(b)]

def guess_noise(dots, step):
    layers = [describe(dots, step)]
    for i in (0, 2):
        layers.append(np.tanh(layers[-1] @ brain[i] + brain[i + 1]))
    return layers[-1] @ brain[4] + brain[5], layers

# 4. TRAIN: add noise we know, ask the brain to guess it, nudge the brain
speed = [np.zeros_like(w) for w in brain]
scale = [np.zeros_like(w) for w in brain]
missed = 0
for turn in range(1, 6001):
    dots, noise = real_dots(512), rng.normal(size=(512, 2))
    step = rng.integers(STEPS, size=512)
    guess, layers = guess_noise(make_noisy(dots, step, noise), step)
    error = guess - noise
    blame = error / len(error)
    for i in (4, 2, 0):
        nudges = [layers[i // 2].T @ blame, blame.sum(0)]
        blame = blame @ brain[i].T * (1 - layers[i // 2] ** 2)
        for j, nudge in zip((i, i + 1), nudges):
            speed[j] = 0.9 * speed[j] + 0.1 * nudge
            scale[j] = 0.999 * scale[j] + 0.001 * nudge ** 2
            brain[j] -= 0.002 * speed[j] / (scale[j] ** 0.5 + 1e-8)
    missed += (error ** 2).mean()
    if turn % 1000 == 0:
        print(f"turn {turn}: error {missed / 1000:.3f}")
        missed = 0

# 5. DRAW: start from pure static, remove a little noise, 50 times
dots = rng.normal(size=(3000, 2))
for step in range(STEPS - 1, -1, -1):
    guess, _ = guess_noise(dots, np.full(len(dots), step))
    dots = dots - add[step] / np.sqrt(1 - keep[step]) * guess
    dots = dots / np.sqrt(1 - add[step])
    if step > 0:
        dots += np.sqrt(add[step]) * rng.normal(size=dots.shape)

# 6. SHOW IT in the terminal
canvas = np.zeros((TALL * 2, WIDE * 4), int)
spot = ((dots + 1) / 2 * [WIDE * 4, TALL * 2]).astype(int)
for x, y in spot:
    if 0 <= x < WIDE * 4 and 0 <= y < TALL * 2:
        canvas[y, x] += 1
for row in canvas:
    print("".join("#" if n > 3 else " " for n in row))
