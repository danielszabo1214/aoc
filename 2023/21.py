
from collections import deque


with open("21.input") as f:
    M = [l.rstrip() for l in f]

pos = None
for row in range(len(M)):
    for col in range(len(M[0])):
        if M[row][col] == "S":
            pos = (row, col)

def neighbors(row, col):
    for i, j in [(0,1), (0,-1), (1,0), (-1,0)]:
        r = row+i
        c = col+j
        if 0 <= r < len(M) and 0 <= c < len(M[r]) and M[r][c] != "#":
            yield (r, c)

q = deque()
q.append((pos, 0))

visited = set()
visited.add(pos)
good = set()
while q:
    p, steps = q.popleft()
    if steps % 2 == 0:
        good.add(p)
    if steps == 64:
        continue

    for neighbor in neighbors(*p):
        if neighbor not in visited:
            q.append((neighbor, steps+1))
            visited.add(neighbor)
        

print(len(good))
