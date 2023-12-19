from collections import defaultdict


words = []

with open("15.input") as f:
    for l in f:
        words = l.rstrip().split(",")

def get_hash(word):
    v = 0
    for c in word:
        ascii = ord(c)
        v += ascii
        v *= 17
        v %= 256
    return v


part1 = 0
for w in words:
    a = get_hash(w)
    # print(w, a)
    part1 += a
print("part1", part1)

m = defaultdict(list)
focals = {}

for w in words:
    if "=" in w:
        label, i = w.split("=")
        h = get_hash(label)
        if label not in m[h]:
            m[h].append(label)
        focals[label] = int(i)
    if "-" in w:
        label, _ = w.split("-")
        h = get_hash(label)
        try:
            m[h].remove(label)
        except:
            pass

part2 = 0
for v, box in m.items():
    for i, label in enumerate(box):
        a = (v+1) * (i+1) * focals[label]
        part2 += a
print("part2", part2)
