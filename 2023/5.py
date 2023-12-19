from dataclasses import dataclass
from typing import List


@dataclass
class SeedRange:
    start: int
    length: int
    
    @property
    def end(self):
        return self.start + self.length - 1
    
    def contains(self, n):
        return self.start <= n < self.start + self.length


@dataclass
class Range:
    source_start: int
    length: int
    dest_start: int

    def apply(self, n):
        if self.source_start <= n < self.source_start + self.length:
            return self.dest_start + n - self.source_start
        else:
            return None
        
    def revert(self, n):
        if self.dest_start <= n < self.dest_start + self.length:
            return self.source_start + n - self.dest_start
        else:
            return None

        
def apply(n, ranges):
    for range in ranges:
        x = range.apply(n)
        if x is not None:
            return x
    return n

def revert(n, ranges):
    for range in ranges:
        x = range.revert(n)
        if x is not None:
            return x
    return n


def run(p, maps):
    for ranges in maps:
        p = apply(p, ranges)
    return p


seeds = []
seed_ranges = []
maps: List[List[Range]] = []


with open("5.arnika") as f:
    for i, line in enumerate(f):
        if i == 0:
            seeds = list(map(int, line.split(": ")[-1].split()))
            for i in range(len(seeds)):
                if i % 2 == 0:
                    seed_ranges.append(SeedRange(seeds[i], seeds[i+1]))
            continue
        
        if not any(char.isdigit() for char in line):
            maps.append([])
            continue

        dest_start, source_start, length = list(map(int, line.split()))
        maps[-1].append(Range(source_start, length, dest_start))


# part 1
arrived = []
for seed in seeds:
    arrived.append(run(seed, maps))
print("part1", min(arrived))

# part 2
def find_min(a, b):
    if a > b:
        return []
    fa = run(a, maps)
    fb = run(b, maps)
    if b - a == fb - fa:
        return [fa]
    else:
        middle = (a + b) // 2
        return find_min(a, middle) + find_min(middle + 1, b)


final_locations2 = []
for seed_range in seed_ranges: 
    m = find_min(seed_range.start, seed_range.end)
    final_locations2.extend(m)
print("part2", min(final_locations2))

# part 2.1
def get_breaking_points(maps: List[List[Range]]):
    range_start_points = []
    for i, ranges in reversed(list(enumerate(maps))):
        range_start_points += [r.source_start for r in ranges]
        if i == 0:
            return list(sorted(set(range_start_points)))
        range_start_points = [revert(s, maps[i-1]) for s in range_start_points]


seed_range_start_points = [seed_range.start for seed_range in seed_ranges]

breaking_points = get_breaking_points(maps)
breaking_points_in_seed_ranges = []
for p in breaking_points:
    for seed_range in seed_ranges:
        if seed_range.contains(p):
            breaking_points_in_seed_ranges.append(p)
            break

final_locations21 = []
for p in seed_range_start_points + breaking_points_in_seed_ranges:
    final_locations21.append(run(p, maps))
print("part 2.1", min(final_locations21))
