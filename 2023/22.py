from collections import defaultdict, deque
from dataclasses import dataclass

@dataclass
class P:
    x: int
    y: int
    z: int

@dataclass
class Brick:
    a: P
    b: P

    def falls_to(self, z):
        self.b.z = z + self.b.z - self.a.z
        self.a.z = z

    def xrange(self):
        s = min(self.a.x, self.b.x)
        e = max(self.a.x, self.b.x) + 1
        return range(s, e)

    def yrange(self):
        s = min(self.a.y, self.b.y)
        e = max(self.a.y, self.b.y) + 1
        return range(s, e)
    
    def zrange(self):
        s = min(self.a.z, self.b.z)
        e = max(self.a.z, self.b.z) + 1
        return range(s, e)
    
    def xy_layer(self):
        s = []
        for x in self.xrange():
            for y in self.yrange():
                s.append((x, y))
        return s

bricks = []

with open("22.input") as f:
    for l in f:
        a, b = l.rstrip().split("~")
        a = list(map(int, a.split(",")))
        b = list(map(int, b.split(",")))
        if a[2] > b[2]:
            a, b = b, a
        bricks.append(Brick(P(*a), P(*b)))

bricks = sorted(bricks, key=lambda b: b.a.z)

# for b in bricks:
#     print(b)

SPACE = defaultdict(lambda:defaultdict(dict))

for i, brick in enumerate(bricks[:]):
    minz = 0
    for (x, y) in brick.xy_layer():
        if SPACE[x][y]:
            z_col = list(SPACE[x][y])[-1]
        else:
            z_col = 0
        minz = max(minz, z_col)
    brick.falls_to(minz+1)
    for (x, y) in brick.xy_layer():
        for z in brick.zrange():
            SPACE[x][y][z] = i

# for z in range(1, 7):
#     print("level", z)
#     for x in range(10):
#         for y in range(10):
#             if z in SPACE[x][y]:
#                 b_id = SPACE[x][y][z]
#                 print(b_id, end="")
#             else:
#                 print(".", end="")
#         print()


def overlap_xy(b1, b2):
    x_overlap1 = b1.a.x <= b2.a.x <= b1.b.x or b1.a.x <= b2.b.x <= b1.b.x
    y_overlap1 = b1.a.y <= b2.a.y <= b1.b.y or b1.a.y <= b2.b.y <= b1.b.y
    x_overlap2 = b2.a.x <= b1.a.x <= b2.b.x or b2.a.x <= b1.b.x <= b2.b.x
    y_overlap2 = b2.a.y <= b1.a.y <= b2.b.y or b2.a.y <= b1.b.y <= b2.b.y
    return (x_overlap1 or x_overlap2) and (y_overlap1 or y_overlap2)

def overlap_xy_slower(b1, b2):
    p1 = b1.xy_layer()
    p2 = b2.xy_layer()
    i = set(p1).intersection(set(p2))
    return len(i) > 0

def bricks_on_top_of(bricks, refbrick):
    level = refbrick.b.z + 1
    on_top = []
    for i, brick in enumerate(bricks):
        if brick.a.z == level:
            if overlap_xy(refbrick, brick):
                on_top.append((i, brick))
    return on_top


def bricks_under(bricks, refbrick):
    level = refbrick.a.z - 1
    under = []
    for i, brick in enumerate(bricks):
        if brick.b.z == level:
            if overlap_xy(refbrick, brick):
                under.append((i, brick))
    return under


def part1():
    removable_count = 0
    for i, brick in enumerate(bricks):
        on_top = bricks_on_top_of(bricks, brick)
        removable = True 
        for j, top_brick in on_top:
            under = bricks_under(bricks, top_brick)
            under_ids = [ii for (ii, _) in under]
            assert i in under_ids, f"{i} not in {under_ids}"
            if under_ids == [i]:
                removable = False

        if removable:
            removable_count += 1
    print(removable_count)

def part2():
    res = 0
    for i in range(len(bricks)):
        q = deque()
        q.append(i)
        removed = set([i])
        while q:
            n = q.popleft()
            top_ids = [i for (i, _) in bricks_on_top_of(bricks, bricks[n])]
            for top_id in top_ids:
                under = bricks_under(bricks, bricks[top_id])
                under_ids = set([ii for (ii, _) in under])
                if under_ids.issubset(removed):
                    removed.add(top_id)
                    q.append(top_id)
        print("i", i, len(removed) - 1)
        res += len(removed) - 1    
    print(res)

part1()
part2()
