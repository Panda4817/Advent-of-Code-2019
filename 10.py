import math
import operator


def process_data(data):
    coords = {}
    lines = [list(line) for line in data.split("\n")]
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                coords[(x, y)] = {"see": 0, "checked": [], "view": []}

    return coords, len(lines[y]), len(lines)


def part1(data):
    asteroids, width, height = process_data(data)
    max_view = 0
    chosen_asteroid = None
    for (x, y) in asteroids.keys():
        for (cx, cy) in asteroids.keys():
            if (x, y) == (cx, cy) or (cx, cy) in asteroids[(x, y)]["checked"]:
                continue
            see = True
            if (x, y) < (cx, cy):
                a = (x, y)
                b = (cx, cy)
            else:
                b = (x, y)
                a = (cx, cy)

            if x == cx:
                for py in range(a[1], b[1] + 1):
                    if (
                        (x, py) in asteroids
                        and (x, py) != (x, y)
                        and (x, py) != (cx, cy)
                    ):
                        see = False
                        break
            elif y == cy:
                for px in range(a[0], b[0] + 1):
                    if (
                        (px, y) in asteroids
                        and (px, y) != (x, y)
                        and (px, y) != (cx, cy)
                    ):
                        see = False
                        break
            else:
                dy = b[1] - a[1]
                dx = b[0] - a[0]
                if abs(dx) != 1 and abs(dy) != 1:
                    while True:
                        for i in range(100, 1, -1):
                            if dx % i == 0 and dy % i == 0:
                                dx = dx // i
                                dy = dy // i
                                break
                        else:
                            break

                for px, py in zip(range(a[0], b[0], dx), range(a[1], b[1], dy)):
                    if (
                        (px, py) in asteroids
                        and (px, py) != (x, y)
                        and (px, py) != (cx, cy)
                    ):
                        see = False
                        break

            if see:
                asteroids[(x, y)]["see"] += 1
                asteroids[(x, y)]["view"].append((cx, cy))
                asteroids[(cx, cy)]["see"] += 1
                asteroids[(cx, cy)]["view"].append((x, y))
            asteroids[(x, y)]["checked"].append((cx, cy))
            asteroids[((cx, cy))]["checked"].append((x, y))

        if asteroids[(x, y)]["see"] > max_view:
            max_view = asteroids[(x, y)]["see"]
            chosen_asteroid = (x, y)

    return (chosen_asteroid, asteroids[chosen_asteroid]["see"])


def part2(data):
    asteroids, cols, rows = process_data(data)
    (start_x, start_y), total = part1(data)
    asteroids_90_0 = []
    asteroids_360_90 = []
    for (x, y) in asteroids.keys():
        if (x, y) == (start_x, start_y):
            continue
        r = math.sqrt(((x - start_x) ** 2) + ((y - start_y) ** 2))
        o = x - start_x
        a = y - start_y
        if x == start_x and y < start_y:
            angle = 90
        elif x == start_x and y > start_y:
            angle = 270
        elif y == start_y and x < start_x:
            angle = 180
        elif y == start_y and x > start_x:
            angle = 0
        else:
            angle = math.degrees(math.atan(o / a))
            if x < start_x and y > start_y:
                angle += 270
            elif x < start_x and y < start_y:
                angle += 90
            elif x > start_x and y > start_y:
                angle += 360

            while angle > 360:
                angle -= 90

            while angle < 0:
                angle += 90

        if 0 <= angle <= 90:
            asteroids_90_0.append([(x, y), r, angle])
        else:
            asteroids_360_90.append([(x, y), r, angle])

    sort_one_90_0 = sorted(asteroids_90_0, key=lambda x: x[1])
    final_sort_90_0 = sorted(sort_one_90_0, key=lambda x: x[2], reverse=True)

    sort_one_360_90 = sorted(asteroids_360_90, key=lambda x: x[1])
    final_sort_360_90 = sorted(sort_one_360_90, key=lambda x: x[2], reverse=True)

    clockwise = final_sort_90_0 + final_sort_360_90

    counter = 0
    goal = 200
    vap_order = []
    while len(vap_order) < len(asteroids) - 1:
        deg_done = []
        for a in clockwise:

            if a[0] in vap_order or a[2] in deg_done:
                continue

            vap_order.append(a[0])
            deg_done.append(a[2])
            counter += 1

        if counter >= goal:
            break

    # for i in range(len(vap_order)):
    #     print(i + 1, " ---- ", vap_order[i])

    x, y = vap_order[goal - 1]
    return x * 100 + y
