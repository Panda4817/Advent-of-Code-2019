class IntcodeComputer:
    def __init__(self, data, input) -> None:
        self.input = input
        self.numbers = [int(i) for i in data.split(",")]
        self.final_output = 0
        self.pointer = 0
        self.relative_base = 0

    def updateInput(self, n):
        self.input = n

    def save_input(self, a, b, c):
        self.numbers[c] = self.input.pop(0)
        return 2

    def get_output(self, a, b, c):
        self.final_output = self.numbers[c]
        return 2

    def add(self, a, b, c):
        self.numbers[c] = self.numbers[a] + self.numbers[b]
        return 4

    def multiply(self, a, b, c):
        self.numbers[c] = self.numbers[a] * self.numbers[b]
        return 4

    def jump_if_true(self, a, b, c):
        if self.numbers[a] != 0:
            return self.numbers[b] - c
        return 3

    def jump_if_false(self, a, b, c):
        if self.numbers[a] == 0:
            return self.numbers[b] - c
        return 3

    def less_than(self, a, b, c):
        if self.numbers[a] < self.numbers[b]:
            self.numbers[c] = 1
        else:
            self.numbers[c] = 0
        return 4

    def equals(self, a, b, c):
        if self.numbers[a] == self.numbers[b]:
            self.numbers[c] = 1
        else:
            self.numbers[c] = 0
        return 4

    def relative_base_offset(self, a, b, c):
        self.relative_base += self.numbers[c]
        return 2

    def unknown(self, a, b, c):
        return 1

    def checkMemory(self, pos):
        try:
            param = self.numbers[pos]
        except IndexError:
            if pos >= 0:
                for i in range(len(self.numbers), pos + 1):
                    self.numbers.append(0)
        param = self.numbers[pos]
        return param

    def identify_mode(self, mode, pointer):
        if mode == 0:
            pos = self.numbers[pointer]
        elif mode == 1:
            pos = pointer
        elif mode == 2:
            pos = self.numbers[pointer] + self.relative_base

        self.checkMemory(pos)
        return pos

    def identify_parameters(self, current_pos):
        modes = [int(i) for i in list(str(self.numbers[current_pos]))]
        while len(modes) < 5:
            modes.insert(0, 0)
        # a, b, c are the parameters, not all opcodes have 3 params
        if modes[-1] == 1:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.identify_mode(modes[0], current_pos + 3)
            func = self.add
        elif modes[-1] == 2:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.identify_mode(modes[0], current_pos + 3)
            func = self.multiply
        elif modes[-1] == 3:
            a = None
            b = None
            c = self.identify_mode(modes[2], current_pos + 1)
            func = self.save_input
        elif modes[-1] == 4:
            a = None
            b = None
            c = self.identify_mode(modes[2], current_pos + 1)
            func = self.get_output
        elif modes[-1] == 5:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = current_pos
            func = self.jump_if_true
        elif modes[-1] == 6:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = current_pos
            func = self.jump_if_false
        elif modes[-1] == 7:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.identify_mode(modes[0], current_pos + 3)
            func = self.less_than
        elif modes[-1] == 8:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.identify_mode(modes[0], current_pos + 3)
            func = self.equals
        elif modes[-1] == 9:
            a = None
            b = None
            c = self.identify_mode(modes[2], current_pos + 1)
            func = self.relative_base_offset
        else:
            # Should never reach if no errors
            a = None
            b = None
            c = None
            func = self.unknown

        # print(self.relative_base, modes, end=" ")
        # if a:
        #     print(self.numbers[current_pos + 1], end=" ")
        # if b:
        #     print(self.numbers[current_pos + 2], end=" ")
        # print(self.numbers[current_pos + 3])
        return a, b, c, func

    def run_program(self):
        while True:
            a, b, c, func = self.identify_parameters(self.pointer)
            jump = func(a, b, c)

            self.pointer += jump
            # print(a, b, c, func.__name__, self.pointer)
            # if a:
            #     print(self.numbers[a], end=" ")
            # if b:
            #     print(self.numbers[b], end=" ")
            # print(self.numbers[c])
            # print()

            if self.numbers[self.pointer] == 99:
                break

            if func.__name__ == "get_output":
                break

        return self.final_output, self.numbers[self.pointer]


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
