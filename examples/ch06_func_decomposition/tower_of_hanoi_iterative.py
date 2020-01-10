#/usr/bin/env/python3

""" towers of hanoi

There is a legend about an Indian temple which contains a large room
with three time-worn posts in it surrounded by 64 golden
disks. Brahmin priests, acting out the command of an ancient prophecy,
have been moving these disks, in accordance with the rules of the
puzzle, since that time. The puzzle is therefore also known as the
Tower of Brahma puzzle. According to the legend, when the last move of
the puzzle is completed, the world will end. (from wikipedia)
"""

import time

### Iterative solution, breaks down at about 20 discs.

def try_move(start, target):
    success = False
    if start != []:
        if (target == []) or (start[-1] > target[-1]):
            success = True
            target.append(start.pop(-1))
    return start, target, success


def find_max(towers):
    maximum = -1
    index = None
    for i in range(len(towers)):
        try:
            if towers[i][-1] > maximum:
                index = i
                maximum = towers[i][-1]
        except Exception:
            pass
    return index


def iterative_solve(towers):
    global moves
    length = len(towers[0])
    maximum = towers[0][-1]
    the_set = set(range(len(towers)))
    last_peg = 0
    solved = False

    if len(towers[0]) % 2 == 0:
        towers[1].append(towers[0].pop(-1))
        towers[2].append(towers[0].pop(-1))
    else:
        towers[2].append(towers[0].pop(-1))
        towers[1].append(towers[0].pop(-1))
    moves += 2

    while not solved:

        move_from = find_max(towers)
        next_peg = (the_set - set([move_from, last_peg])).pop()

        moves += 1
        towers[move_from], towers[next_peg], success = try_move(towers[move_from], towers[next_peg])

        if towers[2] == range(length):
            break

        moves += 1
        tower_last_peg, tower_move_from, success = try_move(towers[last_peg], towers[move_from])
        if success:
            towers[last_peg] = tower_last_peg
            towers[move_from] = tower_move_from
        else:
            towers[move_from], towers[last_peg], success = try_move(towers[move_from], towers[last_peg])

        if towers[2] == range(length):
            break

        last_peg = move_from

    return towers


levels = 2
towers = [[i for i in range(0, levels)], [], []]
moves = 0

benchmark = time.clock()
towers = iterative_solve(towers)
benchmark = time.clock() - benchmark

print("Iterative solution benchmark: %s seconds, made %s moves" % (benchmark, moves))
print("final result: %s" % towers)
print("Optimal solution: %s moves." % (2**levels - 1))
