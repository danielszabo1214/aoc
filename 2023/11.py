from collections import defaultdict


N = []

MAP = []
H_EMPTY = set()
V_EMPTY = set()

with open("11.input") as f:
    for row, l in enumerate(f):
        line = l.rstrip()
        for col, p in enumerate(l):
            if p == "#":
                N.append((row, col))
        MAP.append(line)

print(N)
for row, m in enumerate(MAP):
    if all(map(lambda p: p == ".", m)):
        H_EMPTY.add(row)
    print(m)

for col in range(len(MAP[0])):
    cols = (MAP[row][col] for row in range(len(MAP)))
    if all(map(lambda p: p == ".", cols)):
        V_EMPTY.add(col)

print(H_EMPTY)
print(V_EMPTY)

def node_distance(n1, n2):
    r1, c1 = n1
    r2, c2 = n2

    # print(H_EMPTY)

    h_count = len(list(filter(lambda h: r1 < h < r2 or r1 > h > r2, H_EMPTY)))
    v_count = len(list(filter(lambda v: c1 < v < c2 or c1 > v > c2, V_EMPTY)))
    # print(h_count, v_count)
    return abs(c1-c2) + abs(r1-r2) + (h_count + v_count) * (1000000-1)

dist = defaultdict(dict)
for n1 in N:
    for n2 in N:
        dist[n1][n2] = node_distance(n1, n2)
# print(dist)

# for k in N:
#     for i in N:
#         for j in N:
#              if dist[i][j] > dist[i][k] + dist[k][j]:
#                 dist[i][j] = dist[i][k] + dist[k][j]

# print(dist[(5,1)][(9,4)])
# print(dist[(9,4)][(5,1)])
# print(dist[(0,3)][(8,7)])
# print(dist[(8,7)][(0,3)])
# print(dist[(2,0)][(6,9)])
# print(dist[(6,9)][(2,0)])
# print(dist[(9,0)][(9,4)])
# print(dist[(9,4)][(9,0)])

# print(node_distance((0,3), (8,7)))

part1 = 0
for d in dist.values():
    part1 += sum(d.values())
print("part1", part1 // 2)


# part 2 too high
411143331020
411142919886
# part 2 too low  82000210