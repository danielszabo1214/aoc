from collections import Counter
from dataclasses import dataclass
from functools import cmp_to_key


@dataclass
class Hand:
    cards: str
    bid: int

hands = []
with open("7.input") as f:
    for i, line in enumerate(f):
        cards, bid = line.strip().split()
        hands.append(Hand(cards, int(bid)))


card_strength = ["J"] + list((map(str, range(2, 10))))
card_strength.extend(["T", "Q", "K", "A"])
    

def combinations(cards):
    others = []
    joker_count = 0
    for c in cards:
        if c == "J":
            joker_count += 1
        else:
            others.append(c)
    counter = Counter(others)
    combs = sorted(counter.values(), reverse=True)
    if combs:
        combs[0] += joker_count
    else:
        combs = [joker_count]
    
    return combs

    
def hands_cmp(hand1, hand2):
    cards1 = hand1.cards
    cards2 = hand2.cards
    for c1, c2 in zip(combinations(cards1), combinations(cards2)):
        if c1 == c2:
            continue
        
        return 1 if c1 > c2 else -1
    
    for c1, c2 in zip(cards1, cards2):
        if c1 == c2:
            continue
        return 1 if card_strength.index(c1) > card_strength.index(c2) else -1
    
    raise RuntimeError()

hands.sort(key=cmp_to_key(hands_cmp))
s = 0
for i, hand in enumerate(hands):
    print(i, hand)
    s += (i+1) * hand.bid
print(s)
