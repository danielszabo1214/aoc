
from abc import abstractmethod
from collections import deque
from typing import List, Tuple


L = "low pulse"
H = "high pulse"

B = "broadcaster"


class Module:
    def __init__(self, name, outs):
        self.name = name
        self.outs = outs

    @abstractmethod
    def receive(self, inp: str, pulse: str) -> List[Tuple[bool, str]]:
        pass

class BroadCaster(Module):
    def receive(self, inp: str,  pulse: str):
        return [(self.name, pulse, out) for out in self.outs]

class FlipFlop(Module):
    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.is_on = False

    def receive(self, inp, pulse) -> List[Tuple[bool, str]]:
        if pulse == H:
            return []
        self.is_on = not self.is_on
        return [(self.name, H if self.is_on else L, out) for out in self.outs]

class Conjunction(Module):
    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.remember = {}

    def add_input(self, inp: str):
        self.remember[inp] = L

    def receive(self, inp, pulse) -> List[Tuple[bool, str]]:
        self.remember[inp] = pulse
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


LOW_COUNT = 0
HIGH_COUNT = 0

for i in range(1000):
    q = deque()
    q.append(("button", L, B))

    while q:
        origin, pulse, dest = q.popleft()
        if pulse == H:
            HIGH_COUNT += 1
        else:
            LOW_COUNT +=1

        if dest not in M:
            continue
        for m in M[dest].receive(origin, pulse):
            q.append(m)

print(LOW_COUNT * HIGH_COUNT)