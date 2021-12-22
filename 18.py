from collections import deque
from copy import deepcopy


def process_data(data: str):
    grid = []
    lines = data.split("\n")
    row = []
    x = 0
    y = 0
    start = (x, y)
    door_key = {}

    for line in lines:
        for s in list(line):
            if s == "#":
                row.append(1)
            elif s == ".":
                row.append(0)
            elif s == "@":
                start = (x, y)
                row.append(0)
            else:
                row.append(0)
                door_key[(x, y)] = s
            x += 1

        y += 1
        x = 0
        grid.append(row)
        row = []

    return grid, start, door_key


def part1(data):
    grid, start, door_key = process_data(data)
    print(start)
    print(door_key)
    keys = [i for i in door_key.values() if ord(i) < 65 or ord(i) > 90]
    total_keys = len(keys)
    q = deque([])
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for (dx, dy) in dirs:
        x = start[0] + dx
        y = start[1] + dy
        if grid[y][x] == 0 and (x, y):
            q.append((x, y, 1, set()))

    while q:
        # print(q)
        x, y, steps, collected = q.popleft()
        # print(x, y, steps, collected)
        if (x, y) in door_key:
            if ord(door_key[(x, y)]) >= 65 and ord(door_key[(x, y)]) <= 90:
                if door_key[(x, y)].lower() not in collected:
                    continue
            else:
                collected.add(door_key[(x, y)])

        if len(collected) == total_keys:
            break

        for (dx, dy) in dirs:
            nx = x + dx
            ny = y + dy
            if grid[ny][nx] == 0 and (nx, ny):
                q.append((nx, ny, steps + 1, deepcopy(collected)))

    return steps
