import random

SIZE = 10
# up, right, down, left
MOVES = [(0, -1), (1, 0), (0, 1), (-1, 0)]
# turn left, go straight, turn right
TURNS = (-1, 0, 1)

# 1. THE GAME: a snake, some food, four walls
def place_food(snake):
    while True:
        food = (random.randrange(SIZE), random.randrange(SIZE))
        if food not in snake:
            return food

def blocked(snake, cell):
    x, y = cell
    return not (0 <= x < SIZE and 0 <= y < SIZE) or cell in snake

def step(cell, heading):
    dx, dy = MOVES[heading]
    return (cell[0] + dx, cell[1] + dy)

# 2. WHAT IT SEES (upgraded): is that way a dead end?
def room(snake, start):
    """Free cells reachable from start, counted up to the snake's length."""
    seen, todo = {start}, [start]
    while todo and len(seen) < len(snake):
        cell = todo.pop()
        for heading in range(4):
            nxt = step(cell, heading)
            if nxt not in seen and not blocked(snake, nxt):
                seen.add(nxt)
                todo.append(nxt)
    return len(seen)

def dead_end(snake, cell):
    return blocked(snake, cell) or room(snake, cell) < len(snake)

def see(snake, heading, food):
    (x, y), (fx, fy) = snake[0], food
    ahead = [step(snake[0], (heading + t) % 4) for t in TURNS]
    danger = tuple(dead_end(snake, cell) for cell in ahead)
    return danger + (fx < x, fx > x, fy < y, fy > y, heading)

# 3. ITS MEMORY: one number for every (situation, move)
Q = {}

def best(state):
    return max(TURNS, key=lambda t: Q.get((state, t), 0))

# 4. PLAY ONE GAME, AND LEARN FROM EVERY MOVE
def play(explore):
    snake, heading = [(SIZE // 2, SIZE // 2)], 1
    food, score, hungry, alive = place_food(snake), 0, 0, True
    while alive and hungry < 100:
        state = see(snake, heading, food)
        if random.random() < explore:
            turn = random.choice(TURNS)      # try something
        else:
            turn = best(state)               # use what it knows
        heading = (heading + turn) % 4
        head = step(snake[0], heading)
        reward, hungry = 0, hungry + 1
        if blocked(snake, head):
            reward, alive = -10, False       # crash
        else:
            snake.insert(0, head)
            if head == food:
                reward, score, hungry = 10, score + 1, 0   # food
                food = place_food(snake)
            else:
                snake.pop()
        future = max(Q.get((see(snake, heading, food), t), 0)
                     for t in TURNS) if alive else 0
        old = Q.get((state, turn), 0)
        Q[(state, turn)] = old + 0.1 * (reward + 0.9 * future - old)
    return score

# 5. PRACTICE: thousands of games, fewer random moves each time
if __name__ == "__main__":
    random.seed(0)
    total = 0
    for game in range(1, 3001):
        total += play(explore=max(0.0, 1 - game / 1000))
        if game % 500 == 0:
            print(f"game {game}: average score {total / 500:.1f}")
            total = 0
