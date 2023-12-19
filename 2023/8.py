import math 


lr = ""
directions = {}

with open("8.input") as f:
    s = 0
    for i, line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            lr = line
        else:
            pos, left, right = line.split()
            directions[pos] = (left, right)

print(lr)
print(directions)

# part 1
# pos = "AAA"
# steps = 0
# while pos != "ZZZ":
#     left, right = directions[pos]
#     move = lr[steps % (len(lr))]
#     # print(pos, move, (left,right), steps)
#     steps += 1
#     pos = left if  move == "L" else right

# print("part1", steps)


def run(pos):
    print(pos, end="")
    steps = 0
    while not pos.endswith("Z"):
        left, right = directions[pos]
        move = lr[steps % (len(lr))]
        # print(pos, move, (left,right), steps)
        steps += 1
        pos = left if  move == "L" else right

    print("->", pos, "steps:", steps)
    return steps


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


poss = filter(lambda p: p.endswith("A"), directions.keys())

part2 = 1
for step in map(run, poss):
    part2 = lcm(part2, step)


print("part2", part2)
