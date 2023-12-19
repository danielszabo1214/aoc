import copy
from dataclasses import dataclass
import datetime
import time
from typing import List, Optional


D = []

with open("12.input") as f:
    for l in f:
        line, groups = l.rstrip().split()
        groups = list(map(int, groups.split(",")))
        line = "?".join([line] * 5)
        groups = groups * 5
        D.append((line, groups))


# for part1
def run_part1(line, groups, built):
    if built == "":
        groups_so_far = []
    else:
        groups_so_far = map(len, built.split("."))
        groups_so_far = list(filter(lambda x: x > 0, groups_so_far))
    # print("CC", built, groups_so_far)
    for g1, g2 in zip(groups_so_far[:-1], groups):
        if g1 != g2:
            # print("nope2", built, groups_so_far)
            return 0
    
    if len(built) == len(line):
        if len(groups) == len(groups_so_far) and groups[-1] == groups_so_far[-1]:
            # print("solution", built)
            return 1
        else:
            # print("nope1", built)
            return 0
        
    next_char = line[len(built)]
    if next_char == "?":
        dot = run_part1(line, groups, built + ".")
        hsh = run_part1(line, groups, built + "#")
        return dot + hsh
    else:
        return run_part1(line, groups, built + next_char)

@dataclass
class Block:
    s: int  # size
    b: bool  # still_building
    
def run_part2(line, groups, idx: int, blocks: List[Block], hack: Optional[str]):
    last_block = blocks[-1]
    if idx == len(line):
        if len(blocks)-1 == len(groups) and last_block.s == groups[len(blocks)-2]:
            # print("VALID", blocks)
            return 1
        else:
            return 0
    curr_char = hack or line[idx]
    # print(line, groups, idx, blocks, curr_char)
    if curr_char == ".":
        if last_block.b:
            if last_block.s != groups[len(blocks)-2]:
                return 0
            last_block.b = False
        return run_part2(line, groups, idx+1, copy.deepcopy(blocks), hack=None)
    if curr_char == "#":
        if last_block.b:
            last_block.s += 1
            if last_block.s > groups[len(blocks)-2]:
                return 0
        else:
            if len(blocks)-1 == len(groups):
                return 0
            blocks.append(Block(1, True))
        return run_part2(line, groups, idx+1, blocks, hack=None)
    if curr_char == "?":
        d = run_part2(line, groups, idx, copy.deepcopy(blocks), hack=".")
        h = run_part2(line, groups, idx, copy.deepcopy(blocks), hack="#")
        return d+h

    
COUNT = 0

def run_part3(line, groups, idx: int, built_groups_count, current_group_size, hack: Optional[str]):
    # global COUNT
    # COUNT += 1
    remaining_len = len(line) - idx
    
    if remaining_len == 0:
        if built_groups_count == len(groups):
            return 1
        elif built_groups_count == len(groups)-1 and current_group_size == groups[-1]:
            return 1
        else:
            return 0
        
    remaining_groups = groups[built_groups_count+1:]
    need_at_least = sum(remaining_groups) + len(remaining_groups) - 1

    if remaining_len < need_at_least:
        return 0

    curr_char = hack or line[idx]
    # print(line, groups, idx, blocks, curr_char)
    if curr_char == ".":
        if current_group_size > 0:
            if current_group_size != groups[built_groups_count]:
                return 0
            built_groups_count+=1
            # return run_part3(line, groups, idx+1, built_groups_count+1, 0, hack=None)
        # else:
        return run_part3(line, groups, idx+1, built_groups_count, 0, hack=None)
    if curr_char == "#":
        if current_group_size > 0:
            if current_group_size == groups[built_groups_count]:
                return 0
            return run_part3(line, groups, idx+1, built_groups_count, current_group_size+1, hack=None)
        else:
            if built_groups_count == len(groups):
                return 0
            return run_part3(line, groups, idx+1, built_groups_count, 1, hack=None)
    if curr_char == "?":
        d = run_part3(line, groups, idx, built_groups_count, current_group_size, hack=".")
        h = run_part3(line, groups, idx, built_groups_count, current_group_size, hack="#")
        return d+h
    

def run_part4(line, groups):
    ll = len(line)
    lg = len(groups)
    def _run(idx: int, built_groups_count, current_group_size, hack: Optional[str]=None):
        remaining_len = ll - idx
        
        if remaining_len == 0:
            if built_groups_count == lg:
                return 1
            elif built_groups_count == lg-1 and current_group_size == groups[-1]:
                return 1
            else:
                return 0
            
        # remaining_groups = groups[built_groups_count+1:]
        # need_at_least = sum(remaining_groups) + len(remaining_groups) - 1

        # if remaining_len < need_at_least:
        #     return 0

        curr_char = hack or line[idx]
        # print(line, groups, idx, blocks, curr_char)
        if curr_char == ".":
            if current_group_size > 0:
                if current_group_size != groups[built_groups_count]:
                    return 0
                built_groups_count+=1
            idx +=1
            while idx < ll and line[idx] == ".":
                idx +=1 
            return _run(idx, built_groups_count, 0)
        if curr_char == "#":
            if current_group_size == 0 and built_groups_count == lg:
                return 0
            
            idx += 1
            current_group_size += 1
            while idx < ll and line[idx] == "#":
                idx += 1
                current_group_size += 1
            if current_group_size > groups[built_groups_count]:
                return 0
            return _run(idx, built_groups_count, current_group_size)

        if curr_char == "?":
            d = _run(idx, built_groups_count, current_group_size, hack=".")
            h = _run(idx, built_groups_count, current_group_size, hack="#")
            return d+h
        
    return _run(0, 0, 0, None)


part1 = 0
for i, (line, groups) in enumerate(D[:]):
    # print("INPUT", i, line, groups, "? count", line.count("?"))
    # r = run_part1(line, groups, "")
    # r = run_part2(line, groups, 0, [Block(0, False)], hack=None)
    # r = run_part3(line, groups, 0, 0, 0, hack=None)
    start = time.time()
    print(i, "start", datetime.datetime.now())
    r = run_part4(line, groups)
    print("OUTPU", i, line, groups, r, "{:.2f}s".format(time.time()-start))
    part1 += r
print("part1", part1)


# a = [Block(0, False)]
# print(a)
# b = a[0]
# b.b=True
# print(a)

print("function count call", COUNT)