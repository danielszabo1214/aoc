matches = {}
instances = {}

with open("4.input") as f:
    s = 0
    for i, line in enumerate(f):
        line = line.rstrip()
        game, cards = line.split(": ")
        winning, hand = cards.split(" | ")
        winning_nums = set(winning.split())
        hand_nums = set(hand.split())
        matching = hand_nums.intersection(winning_nums)
        if len(matching):
            # print(matching)
            s += 2 ** (len(matching)-1)
        matches[i] = len(matching)
        instances[i] = 1
print(s)

for i, inst in instances.items():
    m = matches[i]
    for j in range(i+1, i+m+1):
        instances[j] += inst

print(sum(instances.values()))
