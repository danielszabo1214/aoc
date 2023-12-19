from dataclasses import dataclass
from operator import gt, lt

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
            print(name)
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
                    print(rule)
                    expr, dest = rule
                    if part.match(*expr):
                        wf_name = dest
                        break
    res = sum(p.sum() for p in accepted)
    print(res)

part1()
