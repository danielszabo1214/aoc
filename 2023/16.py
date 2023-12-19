from collections import defaultdict


M = []

with open("16.inputt") as f:
    M = [l.rstrip() for l in f]

for m in M:
    print(m)

# import sys
# sys.setrecursionlimit(1500)
# print(sys.getrecursionlimit())


def run(r, c, d):
    visited = defaultdict(set)

    def f2(row, col, dir):
        while True:
            # print("AA", row, col, dir)
            if not 0 <= row < len(M):
                break
            if not 0 <= col < len(M[0]):
                break
            if (row, col) in visited[dir]:
                # print("been here")
                break
        
            visited[dir].add((row, col))

            p = M[row][col]

            if p == "." or (p == "-" and dir in ["left", "right"]) or (p == "|" and dir in ["up", "down"]):
                if dir == "right":
                    col += 1
                if dir == "left":
                    col -= 1
                if dir == "up":
                    row -= 1
                if dir == "down":
                    row += 1
                continue
            elif p == "-" and dir in ["up", "down"]:
                f2(row, col-1, "left")
                f2(row, col+1, "right")
                break
            elif p == "|" and dir in ["left", "right"]:
                f2(row-1, col, "up")
                f2(row+1, col, "down")
                break
            elif p == "\\":
                if dir == "up":
                    col -=1
                    dir = "left"
                elif dir == "down":
                    col += 1 
                    dir = "right"
                elif dir == "left":
                    row -= 1
                    dir = "up"
                elif dir == "right":
                    row += 1 
                    dir = "down"
                continue
            elif p == "/":
                if dir == "up":
                    col +=1
                    dir = "right"
                elif dir == "down":
                    col -= 1
                    dir = "left"
                elif dir == "left":
                    row += 1
                    dir = "down"
                elif dir == "right":
                    row -= 1
                    dir = "up"
                continue
            raise RuntimeError(f"{row} {col} {dir}")

    f2(r, c, d)
    all_visited = set()
    for v in visited.values():
        all_visited.update(v)
    return len(all_visited)

maxi = 0
row_count = len(M)
col_count = len(M[0])

for i in range(row_count):
    r = run(i, 0, "right")
    if r > maxi:
        maxi = r
    r = run(i, col_count - 1, "left")
    if r > maxi:
        maxi = r
for i in range(col_count):
    r = run(0, i, "down")
    if r > maxi:
        maxi = r
    r = run(i, row_count - 1, "up")
    if r > maxi:
        maxi = r
print(maxi)
