from dataclasses import dataclass


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


H = []

WINDOW = (7, 27)
WINDOW = (200000000000000, 400000000000000)

with open("24.input") as f:
    for l in f:
        line = map(int, l.rstrip().split())
        H.append(Hailstone(*line))


def in_window(x, y):
    a, b = WINDOW
    return a <= x <= b and a <= y <= b

def intersect_xy(h1: Hailstone, h2: Hailstone):
    m1 = h1.vy / h1.vx
    a = m1
    c = h1.y - a * h1.x
    m2 = h2.vy / h2.vx
    b = m2
    d = h2.y - b * h2.x
    if a == b:
        return None
    int_x = (d-c) / (a-b)
    if (int_x - h1.x) * h1.vx < 0:
        return None
    if (int_x - h2.x) * h2.vx < 0:
        return None
    int_y = a * int_x + c
    return (int_x, int_y)

def part1():
    c = 0
    for i in range(len(H)):
        for j in range(i+1, len(H)):
            intersection = intersect_xy(H[i], H[j])
            if intersection and in_window(*intersection):
                c += 1
    print(c)
part1()
