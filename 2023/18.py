P = []
max_row = 0
max_col = 0
min_row = 0
min_col = 0
perimeter = 0
with open("18.input") as f:
    row = col = 0
    # P.append((0,0))
    for l in f:
        dir, n, h = l.rstrip().split()
        n = int(n)

        hn, hd = h[:-1], int(h[-1])
        # print(hn, hd)
        dir = "RDLU"[hd]
        n = int(hn, 16)

        perimeter += n 
        new_col = col
        new_row = row
        if dir == "R":
            new_col += n
        if dir == "L":
            new_col -= n
        if dir == "U":
            new_row -= n
        if dir == "D":
            new_row += n
        # P.append(((row, col), (new_row, new_col)))
        row = new_row
        col = new_col
        P.append((row, col))
        max_row = max(max_row, row)
        max_col = max(max_col, col)
        min_row = min(min_row, row)
        min_col = min(min_col, col)

max_row += 1
max_col += 1
print(len(P))
# print(P)
P = [(row-min_row, col-min_col) for (row, col) in P]
max_row -= min_row
max_col -= min_col
print(max_row, max_col, min_row, min_col)


def is_point_in_path(row: int, col: int, poly: list[tuple[int, int]]) -> bool:
    """Determine if the point is on the path, corner, or boundary of the polygon

    Args:
      row -- The row coordinates of point.
      col -- The col coordinates of point.
      poly -- a list of tuples [(row, col), (row, col), ...]

    Returns:
      True if the point is in the path or is a corner or on the boundary"""
    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        # print("POINTS", poly[i], poly[j])
        i_row, i_col = poly[i]
        j_row, j_col = poly[j]
        if (row, col) == poly[i]:
            # point is a corner
            return True
        if i_col == col == j_col and (i_row < row < j_row or i_row > row > j_row):
            return True
        if i_row == row == j_row and (i_col < col < j_col or i_col > col > j_col):
            return True
        if (i_col > col) != (j_col > col):
            slope = (row - i_row) * (j_col - i_col) - (
                j_row - i_row
            ) * (col - i_col)
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (j_col < i_col):
                c = not c
        j = i
    return c

def part1(poly):
    res = 0
    for r in range(max_row):
        for c in range(max_col):
            if is_point_in_path(r, c, poly):
                res += 1
    print(res)


def part2(poly):
    a = 0
    lp = len(poly)
    for i in range(lp):
        j = (i + 1) % lp
        row_i, col_i = P[i]
        row_j, col_j = P[j]
        a += (col_i + col_j) * (row_i - row_j)

    res = (abs(a) // 2)
    return res

# part1(P)
res = part2(P)
print(res + (perimeter // 2) + 1)
