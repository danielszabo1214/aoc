M = []

with open("14.input") as f:
    M = ["#" + l.rstrip() + "#" for l in f]
    M.insert(0, "#" * len(M[0]))
    M.append("#" * len(M[0]))

LM = len(M[0])

# print("ORIGINAL")
# for m in M:
#     print(m)


def load_pointing_left(ms):
    part1 = 0
    for m in ms:
        a = 0
        for i, r in enumerate(m):
            if r == "O":
                a += LM - i - 1
        part1 += a
    return part1


def roll_rocks_left(ms):
    rs = []
    for m in ms:
        groups = m.split("#")
        cs = [g.count("O") for g in groups]
        hs = [i for i, r in enumerate(m) if r=="#"]
        r = ""
        for o_count, hash_pos, next_has_pos in zip(cs[1:], hs, hs[1:] + [LM]):
            r += "#"
            r += "O" * o_count
            r += "." * (next_has_pos - hash_pos - o_count - 1)
        rs.append(r)
    return rs


def clock_wise_rotate(ms, n=1):
    for _ in range(n):
        ms = map(lambda x: "".join(reversed(x)), zip(*ms))
    return list(ms)


print("part1", load_pointing_left(roll_rocks_left(clock_wise_rotate(M, 3))))


def one_cycle(ms):
    for j in range(4):
        # clockwise
        ms = clock_wise_rotate(ms)
        ms = roll_rocks_left(ms)
    return ms


CACHE_ENABLED = False
CACHE_ENABLED = True
CACHE = {}

TARGET = 1000000000
# TARGET = 50
# TARGET = 10

i = 0
ms = clock_wise_rotate(M, 2)
while i < TARGET:
    ms = one_cycle(ms)

    if CACHE_ENABLED:
        k = hash("".join(ms))
        if k in CACHE:
            jump_size = i - CACHE[k]
            # print("YAY", CACHE[k], i)
            i += jump_size * ((TARGET - i) // jump_size)
        else:
            CACHE[k] = i
    i += 1

print("part2", load_pointing_left(clock_wise_rotate(ms)))

# 109328 too high
