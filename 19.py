from intcode import IntcodeComputer


def part1(data):

    w = 50
    h = 50

    total = 0
    for y in range(h):
        for x in range(w):
            comp = IntcodeComputer(data, [x, y])
            out, end = comp.run_program()
            total += out
            if out == 1:
                print("#", end="")
            else:
                print(".", end="")
        print()

    return total


def fit_ship(top_end, data, sq):
    if top_end[0] < 0 or top_end[1] < 0:
        return False
    left_top = (top_end[0] - sq, top_end[1])
    comp = IntcodeComputer(data, [left_top[0], left_top[1]])
    out, end = comp.run_program()
    if out == 0:
        return False
    bottom_left = (top_end[0], top_end[1] + sq)
    comp = IntcodeComputer(data, [bottom_left[0], bottom_left[1]])
    out, end = comp.run_program()
    if out == 0:
        return False
    bottom_right = (top_end[0] + sq, top_end[1] + sq)
    comp = IntcodeComputer(data, [bottom_right[0], bottom_right[1]])
    out, end = comp.run_program()
    if out == 0:
        return False

    return True


def part2(data):
    y = 5
    start = 3
    while True:
        x = start
        found = False
        hit_beam = False
        while True:
            comp = IntcodeComputer(data, [x, y])
            left_top, end = comp.run_program()
            if left_top == 0:
                x += 1
                continue

            if hit_beam == False:
                start = x
                hit_beam = True
            comp = IntcodeComputer(data, [x + 99, y])
            right_top, end = comp.run_program()
            if right_top == 0:
                break
            comp = IntcodeComputer(data, [x, y + 99])
            left_bottom, end = comp.run_program()
            if left_bottom == 1:
                found = True
                break
            else:
                x += 1

        if found:
            break
        y += 1

    return x * 10000 + y
