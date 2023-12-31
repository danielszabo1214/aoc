from collections import defaultdict
import heapq as hq

G = []

with open("17.input") as f:
    G = [list(map(int, l.rstrip())) for l in f]
    
N = defaultdict(list)

for row in range(len(G)):
    for col in range(len(G[0])):
        d = "U"
        w = 0
        for i in range(1, 11):
            if row-i < 0:
                break
            w += G[row-i][col]
            for new_dir in "LR":
                if i > 3:
                    N[(row, col, d)].append(((row-i, col, new_dir), w))
        d = "D"
        w = 0
        for i in range(1, 11):
            if row+i >= len(G):
                break
            w += G[row+i][col]
            for new_dir in "LR":
                if i > 3:
                    N[(row, col, d)].append(((row+i, col, new_dir), w))
        d = "L"
        w = 0
        for i in range(1, 11):
            if col-i < 0:
                break
            w += G[row][col-i]
            for new_dir in "UD":
                if i > 3:
                    N[(row, col, d)].append(((row, col-i, new_dir), w))
        d = "R"
        w = 0
        for i in range(1, 11):
            if col+i >= len(G[0]):
                break
            w += G[row][col+i]
            for new_dir in "UD":
                if i > 3:
                    N[(row, col, d)].append(((row, col+i, new_dir), w))

q = []

st = (0, 0, "D")  # or "R" as these are the 2 directions from (0, 0)

dist = {}
parent = {}

visited = set()
hq.heappush(q, (0, st))

end_node = None

while q:
    dist_to_n, n = hq.heappop(q)
    visited.add(n)

    nrow, ncol, ndir = n
    if nrow == len(G)-1 and ncol == len(G[0])-1:
        end_node = n
        print(dist_to_n)
        break

    for neighbor in N[n]:
        m, w = neighbor
        if m not in visited:
            dist_to_m = dist_to_n + w
            if m not in dist or dist_to_m <= dist[m]:
                dist[m] = dist_to_m
                parent[m] = n
                hq.heappush(q, (dist_to_m, m))
