# Time:      7  15   30
# Distance:  9  40  200

# Time:        62     73     75     65
# Distance:   644   1023   1240   1023

races = [(7,9), (15,40), (30,200)]
races = [(62,644), (73,1023), (75,1240), (65,1023)]

def win_race(time, distance):
    options = 0
    for t in range(time):
        if t * (time - t) > distance:
            options += 1
    return options

part1 = 1
for time, distance in races:
    part1 *= win_race(time, distance)

print("part1", part1)

# part 2
time, distance = race = (71530, 940200)
time, distance = race = (62737565, 644102312401023)

part2 = win_race(time, distance)
print("part2", part2)
