numbers = {}
symbols = {}

with open("3.input") as f:
    for i, line in enumerate(f):
        line = line.rstrip()
        j = 0
        while j < len(line):
            c = line[j]
            number = []
            if j == ".":
                continue
            number_pos = None
            if c.isnumeric():
                while c.isnumeric():
                    if not number_pos:
                        number_pos = (i, j)
                    number.append(c)
                    j += 1
                    if j < len(line):
                        c = line[j]
                    else:
                        break
                numbers[number_pos] = int("".join(number))
            if c == "*":
                symbols[(i, j)] = c
            j += 1

print(numbers)
print(symbols)

def neighbors(pos, num):
    l = len(str(num))
    row, col = pos
    res = set()
    for i in [row-1, row, row+1]:
        for j in range(-1, l+1):
            res.add((i, col+j))
    return res

s = 0
for pos, num in numbers.items():
    ns = neighbors(pos, num)
    gears_next_to_num = neighbors(pos, num).intersection(symbols.keys())
    for pos1, num1 in numbers.items():
        if pos == pos1:
            continue
        gears_next_to_num1 = neighbors(pos1, num1).intersection(symbols.keys())
        gear_pos = gears_next_to_num.intersection(gears_next_to_num1)
        if gear_pos:
            s += num * num1
print(s//2)
