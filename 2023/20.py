
from abc import abstractmethod
from collections import deque
import math
from typing import List, Tuple


L = "L"
H = "H"

B = "broadcaster"


class Module:
    def __init__(self, name, outs):
        self.name = name
        self.outs = outs

    @abstractmethod
    def receive(self, i, inp: str, pulse: str) -> List[Tuple[bool, str]]:
        pass

class BroadCaster(Module):
    def receive(self, i, inp: str,  pulse: str):
        return [(self.name, pulse, out) for out in self.outs]

class FlipFlop(Module):
    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.is_on = False

    def receive(self, i, inp, pulse) -> List[Tuple[bool, str]]:
        if pulse == H:
            return []
        self.is_on = not self.is_on
        return [(self.name, H if self.is_on else L, out) for out in self.outs]

class Conjunction(Module):
    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.remember = {}
        self.nums = {}

    def add_input(self, inp: str):
        self.remember[inp] = L
        self.nums[inp] = []

    def receive(self, i, inp, pulse) -> List[Tuple[bool, str]]:
        self.remember[inp] = pulse
        if pulse == "H":
            self.nums[inp].append(i)
        if self.name == "gf":
            pulses = "".join(self.remember.values())
            if pulses != "LLLL":
                print("found", self.nums)
            # print("gf", pulses)
        all_h = all(rem == H for rem in self.remember.values())
        return [(self.name, L if all_h else H, out) for out in self.outs]


M = {}
conjunctions = []
with open ("20.input") as f:
    for l in f:
        line = l.rstrip().split()
        name = line[0]
        op, n = name[0], name[1:]
        if name == B:
            M[name] = BroadCaster(name, line[1:])
        elif op == "%":
            M[n] = FlipFlop(n, line[1:])
        elif op == "&":
            M[n] = Conjunction(n, line[1:])
            conjunctions.append(n)

for name, mo in M.items():
    for out in mo.outs:
        if out in conjunctions:
            M[out].add_input(name)


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def part1():
    LOW_COUNT = 0
    HIGH_COUNT = 0

    for i in range(1, 5000):
        q = deque()
        q.append(("button", L, B))

        while q:
            origin, pulse, dest = q.popleft()
            # for part1
            if i <= 1000:
                if pulse == H:
                    HIGH_COUNT += 1
                else:
                    LOW_COUNT +=1

            if dest not in M:
                continue
            for m in M[dest].receive(i, origin, pulse):
                q.append(m)

    print(LOW_COUNT * HIGH_COUNT)

part1()

part2 = 1
# this list contains how often the inputs of &gf are enabled
for i in [4051, 3919, 3761, 3907]:
    part2 = lcm(part2, i)
print(part2)
