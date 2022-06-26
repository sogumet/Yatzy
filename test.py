import itertools

hand = [1, 2, 1, 4, 1, 2]
out = itertools.combinations(hand, 3)
for x in out:
    if x.count(x[0]) == len(x):
        print(x[0])


