from intcode import IntcodeComputer
from collections import deque
from copy import deepcopy


def part1(data):

    current = (0, 0)
    visited_free = set()
    visited_free.add(current)
    visited_walls = set()
    q = deque(
        [
            ((0, -1), 1, IntcodeComputer(data, 1)),
            ((0, 1), 1, IntcodeComputer(data, 2)),
            ((-1, 0), 1, IntcodeComputer(data, 3)),
            ((1, 0), 1, IntcodeComputer(data, 4)),
        ]
    )
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while q:
        (x, y), steps, comp = q.popleft()
        output, num = comp.run_program()
        if output == 2:
            break
        elif output == 0:
            visited_walls.add((x, y))
            continue
        elif output == 1:
            visited_free.add((x, y))
            d = 1
            for (dx, dy) in dirs:
                temp = (x + dx, y + dy)
                if temp not in visited_walls and temp not in visited_free:
                    copycomp = deepcopy(comp)
                    copycomp.updateInput(d)
                    q.append((temp, steps + 1, copycomp))
                d += 1

    return steps


def part2(data):
    current = (0, 0)
    visited_free = set()
    visited_free.add(current)
    visited_walls = set()
    q = deque(
        [
            ((0, -1), 1, IntcodeComputer(data, 1)),
            ((0, 1), 1, IntcodeComputer(data, 2)),
            ((-1, 0), 1, IntcodeComputer(data, 3)),
            ((1, 0), 1, IntcodeComputer(data, 4)),
        ]
    )
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while q:
        (x, y), steps, comp = q.popleft()
        output, num = comp.run_program()
        if output == 0:
            visited_walls.add((x, y))
            continue
        elif output == 1 or output == 2:
            if output == 2:
                oxygen = (x, y)
            visited_free.add((x, y))
            d = 1
            for (dx, dy) in dirs:
                temp = (x + dx, y + dy)
                if temp not in visited_walls and temp not in visited_free:
                    copycomp = deepcopy(comp)
                    copycomp.updateInput(d)
                    q.append((temp, steps + 1, copycomp))
                d += 1
    all = set.union(visited_free, visited_walls)
    lowest_x = min([c[0] for c in all])
    highest_x = max([c[0] for c in all])
    lowest_y = min([c[1] for c in all])
    highest_y = max([c[1] for c in all])

    for y in range(lowest_y, highest_y + 1):
        for x in range(lowest_x, highest_x + 1):
            if (x, y) == (0, 0):
                print("D", end="")
            elif (x, y) == oxygen:
                print("O", end="")
            elif (x, y) in visited_walls:
                print("#", end="")
            elif (x, y) in visited_free:
                print(".", end="")

            else:
                print(" ", end="")
        print()

    q.append((oxygen, 0))
    visited_free.remove(oxygen)
    while q:
        (x, y), time = q.popleft()
        for (dx, dy) in dirs:
            temp = (x + dx, y + dy)
            try:
                visited_free.remove(temp)
                q.append((temp, time + 1))
            except KeyError:
                continue

    return time
