from collections import deque

DIRS = []
MAP = []

with open("10.input") as f:
    for i, l in enumerate(f):
        line = l.rstrip()
        directions = []
        for j, d in enumerate(line):
            if d == ".":
                directions.append([])
            elif d == "|":
                directions.append(["up", "down"])
            elif d == "-":
                directions.append(["left", "right"])
            elif d == "L":
                directions.append(["up", "right"])
            elif d == "J":
                directions.append(["up", "left"])
            elif d == "7":
                directions.append(["down", "left"])
            elif d == "F":
                directions.append(["down", "right"])
            elif d == "S":
                directions.append(["S"])
                pos = (i, j)
        DIRS.append(directions)
        m = []
        for i in line:
            m.append(i)
        MAP.append(m)

NROW = len(DIRS)
NCOL = len(DIRS[0])

print(NROW, NCOL)

def get_next_dir(row, col, dir):
    d = DIRS[row][col]
    if d == ["S"]:
        return "HOME"
    dir_from_other_side = {
        "up": "down",
        "down": "up",
        "left": "right",
        "right": "left",
    }
    dir = dir_from_other_side[dir]
    if dir in d:
        if dir == d[0]:
            return d[1]
        else:
            return d[0]
    return None


def run_part1(row, col, dir):
    start_row = row
    start_col = col
    steps = 0
    first = True
    while (not (start_row == row and start_col == col)) or first:
        first = False
        if dir == "up":
            row -= 1
        elif dir == "down":
            row += 1
        elif dir == "left":
            col -= 1
        elif dir == "right":
            col += 1

        if not (0 <= row < NROW and 0 <= col < NCOL):
            print("exit1")
            return (False, 0)
        
        dir = get_next_dir(row, col, dir)
        if dir is None:
            print("exit2")
            return (False, 0)
        steps += 1

    return (True, steps)


r, c = pos
hack = set()
for d in ["up", "down", "left", "right"]:
    possible, steps = run_part1(r, c, d)
    if possible:
        hack.add(d)
        print("part 1", steps // 2)

print(hack)
if hack == set(["up", "down"]):
    MAP[r][c] = "|"
if hack == set(["up", "left"]):
    MAP[r][c] = "J"
if hack == set(["up", "right"]):
    MAP[r][c] = "L"
if hack == set(["down", "left"]):
    MAP[r][c] = "7"
if hack == set(["down", "right"]):
    MAP[r][c] = "F"
if hack == set(["left", "right"]):
    MAP[r][c] = "-"

def run_part2(row, col, dir):
    start_row = row
    start_col = col
    steps = 0
    first = True
    upscaled_loop = set([(2*row+1, 2*col+1)])
    while (not (start_row == row and start_col == col)) or first:
        first = False
        if dir == "up":
            upscaled_loop.add((2*row, 2*col+1))
            row -= 1
            upscaled_loop.add((2*row+1, 2*col+1))
        elif dir == "down":
            row += 1
            upscaled_loop.add((2*row, 2*col+1))
            upscaled_loop.add((2*row+1, 2*col+1))
        elif dir == "left":
            upscaled_loop.add((2*row+1, 2*col))
            col -= 1
            upscaled_loop.add((2*row+1, 2*col+1))
        elif dir == "right":
            col += 1
            upscaled_loop.add((2*row+1, 2*col))
            upscaled_loop.add((2*row+1, 2*col+1))

        if not (0 <= row < NROW and 0 <= col < NCOL):
            print("exit1")
            return (False, 0, set())
        
        dir = get_next_dir(row, col, dir)
        if dir is None:
            print("exit2")
            return (False, 0, set())
        steps += 1
    print("dir", dir)
    return (True, steps, upscaled_loop)

r, c = pos
for d in ["up", "down", "left", "right"]:
    possible, steps, loop = run_part2(r, c, d)
    if possible:
        print("part 2", steps, len(loop) )
        break

# raise RuntimeError()

G = []
for _ in range(2*NROW+1):
    G.append([" "] * (2*NCOL+1))

for row in range(NROW):
    for col in range(NCOL):
        G[2*row+1][2*col+1] = MAP[row][col]


outside = 0
q = deque()

q.append((0, 0))
visited = set([(0, 0)])

while q:
    row, col = q.popleft()
    
    if G[row][col] != " ":
        outside += 1

    for (i, j) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r = row+i
        c = col+j
        if 0 <= r < len(G) and 0 <= c < len(G[0]):
            pos = (r, c)
            if (pos not in loop) and pos not in visited:
                q.append(pos)
                visited.add(pos)

print("part2", NCOL*NROW - outside - len(loop)//2)
