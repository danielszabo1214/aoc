from collections import defaultdict, deque


gr = []
G = defaultdict(set)

with open("25.input") as f:
    gr.append("digraph mygraph {")
    for l in f:
        l = l.rstrip().split()
        a = l[0]
        for b in l[1:]:
            gr.append(f"  {a} -> {b}")
            G[a].add(b)
            G[b].add(a)

    gr.append("}")

# for l in gr:
#     print(l)

PATHS = set()

def bfs(fr, to):
    q = deque()
    q.append(fr)
    visited = set()
    visited.add(fr)
    parents = {}

    found = False
    while q:
        n = q.popleft()
        if n == to:
            found = True
            break

        for neighbor in G[n]:
            if (n, neighbor) in PATHS:
                continue
            if neighbor not in visited:
                q.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = n

    if found:
        n = to
        while n in parents:
            p = parents[n]
            PATHS.add((p, n))
            n = p

    return visited

bfs("ccs", "ckb")
bfs("ccs", "ckb")
bfs("ccs", "ckb")
visited = bfs("ccs", "ckb")

print(len(visited) * (len(G)-len(visited)))
