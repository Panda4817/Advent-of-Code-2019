from intcode import IntcodeComputer


def part1(data):
    comp = IntcodeComputer(data, [0])
    outputs = []
    out, end = comp.run_program()
    outputs.append(out)
    while end != 99:
        out, end = comp.run_program()
        outputs.append(out)

    grid = []
    row = []
    for n in outputs:
        if n == 35:
            row.append(1)
            print("#", end="")
        elif n == 46:
            row.append(0)
            print(".", end="")
        elif n == 10:
            grid.append(row)
            print()
            row = []
        else:
            print("^", end="")
            row.append(1)

    grid = grid[0:-2]

    al = 0
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[r]) - 1):
            if grid[r][c] != 1:
                continue
            for (dx, dy) in dirs:
                if grid[r + dy][c + dx] != 1:
                    break
            else:
                al += r * c

    return al, grid


def part2(data):
    comp = IntcodeComputer(data, [])
    comp.numbers[0] = 2
    al, grid = part1(data)
    h = len(grid)
    w = len(grid[0])
    path = []
    robot = (4, 0)

    facing = "u"
    dirs = {
        "u": [(0, -1), "l", "r"],
        "d": [(0, 1), "r", "l"],
        "l": [(-1, 0), "d", "u"],
        "r": [(1, 0), "u", "d"],
    }

    steps = 0
    while True:
        temp = (robot[0] + dirs[facing][0][0], robot[1] + dirs[facing][0][1])
        if (
            temp[0] < 0
            or temp[0] == w
            or temp[1] < 0
            or temp[1] == h
            or grid[temp[1]][temp[0]] != 1
        ):
            if steps > 0:
                path.append(steps)
                steps = 0

            for i in range(1, 3):
                tf = dirs[facing][i]
                temp = (robot[0] + dirs[tf][0][0], robot[1] + dirs[tf][0][1])
                # print(temp, grid[temp[1]][temp[0]])
                try:
                    if grid[temp[1]][temp[0]] == 1:
                        if i == 1:
                            path.append("L")
                        else:
                            path.append("R")
                        facing = tf
                        break
                except IndexError:
                    pass
            else:
                break

        steps += 1
        robot = temp

    print(path)

    A = "L,4,L,4,L,10,R,4\n"
    B = "R,4,L,4,L,4,R,8,R,10\n"
    C = "R,4,L,10,R,10\n"

    main = "A,B,A,C,A,C,B,C,C,B\n"

    main_asci = [ord(s) for s in main]
    a_asci = []
    for s in A:
        a_asci.append(ord(s))

    b_asci = []
    for s in B:
        b_asci.append(ord(s))

    c_asci = []
    for s in C:
        c_asci.append(ord(s))

    main_asci.extend(a_asci)
    main_asci.extend(b_asci)
    main_asci.extend(c_asci)
    main_asci.append(ord("n"))
    main_asci.append(10)
    out, end = comp.run_program()
    print(chr(out), end="")
    outputs = []
    while end != 99:
        out, end = comp.run_program()
        print(chr(out), end="")
        outputs.append(out)
        if chr(out) == ":":
            comp.updateInput(main_asci)

    return outputs[-1]
