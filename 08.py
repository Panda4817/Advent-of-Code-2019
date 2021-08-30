import sys


def process_data(data, rows, cols):
    pixels = [int(i) for i in data]
    layers = []
    min_zero_count = sys.maxsize
    ones_mul_twos = 0
    while pixels:
        layer = []
        zero_count = 0
        one_count = 0
        two_count = 0
        for r in range(rows):
            row = []
            for c in range(cols):
                n = pixels.pop(0)
                if n == 0:
                    zero_count += 1
                elif n == 1:
                    one_count += 1
                elif n == 2:
                    two_count += 1
                row.append(n)
            layer.append(row)
        layers.append(layer)

        if zero_count < min_zero_count:
            min_zero_count = zero_count
            ones_mul_twos = one_count * two_count

    return layers, ones_mul_twos


# Part 2 in part1
def part1(data):
    cols = 25
    rows = 6
    layers, part1_ans = process_data(data, rows, cols)
    print("Part 2 - Password is: ")
    for r in range(rows):
        for c in range(cols):
            pixel = -1
            for layer in layers:
                if (layer[r][c] == 0 or layer[r][c] == 1) and pixel == -1:
                    pixel = layer[r][c]
                continue

            if pixel == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    return part1_ans
