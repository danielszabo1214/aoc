from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from operator import gt, lt
import pprint

@dataclass
class R:
    mi: int
    ma: int

    @property
    def vol(self):
        return self.ma - self.mi

@dataclass
class Cube:
    x: R
    m: R
    a: R
    s: R

    @property
    def vol(self):
        return self.x.vol * self.m.vol * self.a.vol * self.s.vol

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def match(self, op, attr, v):
        return op(getattr(self, attr), v)
    
    def sum(self):
        return self.x + self.m + self.a + self.s
    
WF = {}
PARTS = []

with open("19.input") as f:
    wfs = True
    for l in f:
        l = l.rstrip()
        if l == "":
            wfs = False
            continue
        if wfs:
            name, rules = l[:-1].split("{")
            rs = []
            for rule in rules.split(","):
                if ":" not in rule:
                    rs.append(rule)
                else:
                    ineq, dest = rule.split(":")
                    if ">" in ineq:
                        a, b = ineq.split(">")
                        if a.isalpha():
                            rs.append(((gt, a, int(b)), dest))
                        else:
                            rs.append(((gt, b, int(a)), dest))
                    if "<" in ineq:
                        a, b = ineq.split("<")
                        if a.isalpha():
                            rs.append(((lt, a, int(b)), dest))
                        else:
                            rs.append(((lt, b, int(a)), dest))
            WF[name] = rs
        else:
            PARTS.append(Part(*map(int, l.split())))

def part1():
    accepted = []
    for part in PARTS:
        wf_name = "in"
        while True:
            if wf_name == "A":
                accepted.append(part)
                break
            if wf_name == "R":
                break

            for rule in WF[wf_name]:
                if isinstance(rule, str):
                    wf_name = rule
                else:
                    expr, dest = rule
                    if part.match(*expr):
                        wf_name = dest
                        break
    res = sum(p.sum() for p in accepted)
    print(res)

part1()

def split(cube, op, attr, v):
    range = getattr(cube, attr)
    if op == lt:
        if range.ma <= v:
            return cube, None
        if v < range.mi:
            return None, cube
        tr = deepcopy(cube)
        fa = deepcopy(cube)
        setattr(tr, attr, R(range.mi, v))
        setattr(fa, attr, R(v, range.ma))
        return tr, fa
    if op == gt:
        if range.mi > v:
            return cube, None
        if v >= range.ma:
            return None, cube
        tr = deepcopy(cube)
        fa = deepcopy(cube)
        setattr(tr, attr, R(v+1, range.ma))
        setattr(fa, attr, R(range.mi, v+1))
        return tr, fa


def split_cube(cube, rules):
    res = defaultdict(list)
    for rule in rules:
        if isinstance(rule, str):
            res[rule].append(cube)
            break
        expr, dest = rule
        tr, fa = split(cube, *expr)
        cube = fa
        res[dest].append(tr)

    return res


def part2():
    accepted = []
    cube = Cube(R(1, 4001),R(1, 4001),R(1, 4001),R(1, 4001))

    q = deque()
    q.append(("in", cube))
    while q:
        name, c = q.popleft()
        for new_name, new_cs in split_cube(c, WF[name]).items():
            for new_c in new_cs:
                if new_name == "A":
                    accepted.append(new_c)
                elif new_name == "R":
                    continue
                else:
                    q.append((new_name, new_c))
    res = 0
    for a in accepted:
        res += a.vol
    print(res)
part2()
