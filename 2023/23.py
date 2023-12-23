
from collections import deque
import copy
import functools


with open("23.input") as f:
    M = [l.rstrip() for l in f]

NROW = len(M)
NCOL = len(M[0])

start_col = M[0].index(".")
START = (0, start_col)

end_col = M[-1].index(".")
END = (NROW-1, end_col)

print(START, END)

@functools.cache
def get_neighbours(row, col):
    res = []
    for (i, j) in [(0, 1), (0, -1), (1, 0), (-1, 0)][::-1]:
        r = row + i
        c = col + j
        if 0 <= r < NROW and 0 <= c < NCOL:
            if M[r][c] != "#":
                res.append((r, c))
    return res


MAX_STEP_COUNTS = 0

def slide(row, col):
    v = M[row][col]
    if v == "<":
        return (row, col - 1)
    if v == ">":
        return (row, col + 1)
    if v == "^":
        return (row - 1, col)
    if v == "v":
        return (row + 1, col)
    return None

def dijkstra_possible(path, pos):
    q = deque()
    visited = set()

    q.append(pos)
    visited.add(pos)

    while q:
        row, col = q.popleft()
        if row == NROW - 1:
            return True
        
        for n in get_neighbours(row, col):
            nrow, _ = n
            if nrow == NROW - 1:
                return True
            if n not in path and n not in visited:
                q.append(n)
                visited.add(n)
    return False

i = 0

def f(path, current_pos):
    while True:
        path.add(current_pos)
        row, _ = current_pos
        if row == NROW - 1:
            global MAX_STEP_COUNTS
            MAX_STEP_COUNTS = max(MAX_STEP_COUNTS, len(path)-1)
            global i
            if i % 100 == 0:
                print(i, "DONE", MAX_STEP_COUNTS)
            i += 1
            return

        # part1
        # slide_pos = slide(*current_pos)
        # if slide_pos:
        #     possible_nexts = [slide_pos]
        # else:
        #     possible_nexts = get_neighbours(*current_pos)

        # part2
        # a bit slow: a few hours
        possible_nexts = get_neighbours(*current_pos)

        nexts = []
        for n in possible_nexts:
            if n not in path:
                nexts.append(n)
        
        if len(nexts) == 1:
            current_pos = nexts[0]
        else:
            nexts2 = []
            for n in nexts:
                if dijkstra_possible(path, n):
                    nexts2.append(n)
            if len(nexts2) == 1:
                current_pos = nexts2[0]
            else:
                for n in nexts2:
                    f(copy.deepcopy(path), n)
                break

f(set(), START)

print(MAX_STEP_COUNTS)

