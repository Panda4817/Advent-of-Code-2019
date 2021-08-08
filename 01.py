from math import floor


def process_data(data):
    return [int(i) for i in data.split("\n")]


def fuel(m):
    return floor(m / 3) - 2


def part1(data):
    modules = process_data(data)
    total = 0
    for m in modules:
        total += fuel(m)

    return total


def recurse_fuel(total, m):
    f = fuel(m)
    if f == 0 or f < 0:
        return total

    total += f
    total = recurse_fuel(total, f)

    return total


def part2(data):
    modules = process_data(data)
    total = 0
    for m in modules:
        total = recurse_fuel(total, m)

    return total
