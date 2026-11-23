import math, random

BIRDS, KEEP, GOAL = 100, 10, 1000
GAP, BIRD_X = 0.30, 0.2

# 1. THE GAME: pipes slide left, each with a gap at a random height
def new_pipe():
    return [1.0, random.uniform(0.25, 0.75)]

# 2. THE BRAIN: 25 numbers. 4 things it sees -> 4 neurons -> flap?
def new_brain():
    return [random.uniform(-1, 1) for _ in range(25)]

def wants_to_flap(brain, sees):
    neurons = []
    for n in range(4):
        w = brain[n * 5:n * 5 + 5]
        total = sum(a * b for a, b in zip(w, sees)) + w[4]
        neurons.append(math.tanh(total))
    vote = sum(a * b for a, b in zip(brain[20:24], neurons))
    return vote + brain[24] > 0

# 3. ONE GENERATION: every bird flies the same course
def fly(brains):
    height = [0.5] * len(brains)
    speed = [0.0] * len(brains)
    lived = [0] * len(brains)
    alive = set(range(len(brains)))
    pipes, passed, frame = [new_pipe()], 0, 0
    while alive and passed < GOAL:
        frame += 1
        for pipe in pipes:
            pipe[0] -= 0.012
        if pipes[0][0] < BIRD_X - 0.06:
            pipes.pop(0)
            passed += 1
        if pipes[-1][0] < 0.28:
            pipes.append(new_pipe())
        x, gap = pipes[0]
        for b in list(alive):
            sees = (height[b], gap, speed[b] * 20, x - BIRD_X)
            if wants_to_flap(brains[b], sees):
                speed[b] = -0.022                    # flap
            speed[b] += 0.0016                       # gravity
            height[b] += speed[b]
            at_pipe = abs(x - BIRD_X) < 0.06
            in_gap = abs(height[b] - gap) < GAP / 2
            in_sky = 0 < height[b] < 1
            if (at_pipe and not in_gap) or not in_sky:
                alive.remove(b)                # crashed
                lived[b] = frame
    for b in alive:
        lived[b] = frame
    return lived, passed

# 4. EVOLUTION: copy a winner, change every number a little
def child(parent):
    return [w + random.gauss(0, 0.3) for w in parent]

# 5. RUN: keep evolving, even after the first perfect flight
GENERATIONS = 30

random.seed(3)
brains = [new_brain() for _ in range(BIRDS)]
for generation in range(1, GENERATIONS + 1):
    lived, passed = fly(brains)
    print(f"generation {generation}: best bird passed {passed}")
    order = sorted(range(BIRDS), key=lambda b: -lived[b])
    best = [brains[b] for b in order[:KEEP]]
    brains = best + [child(random.choice(best)) for _ in range(90)]

# 6. THE EXAM: the champion alone, on 30 courses it has never seen
perfect = 0
for course in range(30):
    lived, passed = fly([best[0]])
    perfect += passed == GOAL
print(f"exam: perfect on {perfect} of 30 new courses")
