lines = []

with open("9.input") as f:
    for line in f:
        lines.append(list(map(int, line.rstrip().split())))

part1 = 0
part2 = 0
for line in lines:
    pyramid = []
    pyramid.append(line)
    print("line", line)
    while not all(map(lambda x: x == 0, pyramid[-1])):
        p = [b - a for a, b in zip(pyramid[-1], pyramid[-1][1:])]
        pyramid.append(p)

    part1 += sum(p[-1] for p in pyramid)
    
    # first_nums = (p[0] for p in pyramid)
    zeroth = 0
    for i, num in enumerate(p[0] for p in pyramid):
        sign = 1 if i % 2 == 0 else -1
        zeroth += sign * num
    part2 += zeroth
print("part1", part1)
print("part2", part2)
