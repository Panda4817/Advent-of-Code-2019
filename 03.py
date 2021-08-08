import sys


def process_path(part):
    l = part[0]
    steps = int(part[1:])
    if l == "R":
        direction = (1, 0, steps)
    elif l == "L":
        direction = (-1, 0, steps)
    elif l == "U":
        direction = (0, 1, steps)
    elif l == "D":
        direction = (0, -1, steps)

    return direction


def process_data(data):
    lines = data.split("\n")
    wire_a = []
    for part in lines[0].split(","):
        direction = process_path(part)
        wire_a.append(direction)

    wire_b = []
    for part in lines[1].split(","):
        direction = process_path(part)
        wire_b.append(direction)

    return wire_a, wire_b


def part1(data):
    wire_a, wire_b = process_data(data)
    coords_a = set()
    current = [0, 0]
    for x, y, steps in wire_a:
        for i in range(steps):
            current[0] += x
            current[1] += y
            coords_a.add(tuple(current))

    current = [0, 0]
    coords_b = set()
    for x, y, steps in wire_b:
        for i in range(steps):
            current[0] += x
            current[1] += y
            coords_b.add(tuple(current))

    lowest_dist = sys.maxsize
    intersections = coords_a.intersection(coords_b)
    for k in intersections:
        mh = abs(k[0]) + abs(k[1])
        if mh < lowest_dist:
            lowest_dist = mh

    return lowest_dist, intersections


def part2(data):
    wire_a, wire_b = process_data(data)
    lowest_dist, intersections = part1(data)
    total_steps = sys.maxsize
    for i in intersections:
        current = [0, 0]
        steps_a = 0
        for x, y, steps in wire_a:
            found = False
            for j in range(steps):
                current[0] += x
                current[1] += y
                steps_a += 1
                if tuple(current) == i:
                    found = True
                    break

            if found:
                break

        current = [0, 0]
        steps_b = 0
        for x, y, steps in wire_b:
            found = False
            for j in range(steps):
                current[0] += x
                current[1] += y
                steps_a += 1
                if tuple(current) == i:
                    found = True
                    break

            if found:
                break

        total = steps_a + steps_b
        if total < total_steps:
            total_steps = total

    return total_steps
