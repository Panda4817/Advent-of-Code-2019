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
        self.numbers[c] = self.input
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


class Robot:
    def __init__(self, data, input) -> None:
        self.painted_panels = {}
        self.robot_pos = (0, 0)
        self.output_nums = []
        self.dir = "u"
        self.dirs = {
            "u": [(0, -1), "l", "r"],
            "d": [(0, 1), "r", "l"],
            "l": [(-1, 0), "d", "u"],
            "r": [(1, 0), "u", "d"],
        }
        self.brain = IntcodeComputer(data, input)

    def moveForward(self):
        self.robot_pos = (
            self.robot_pos[0] + self.dirs[self.dir][0][0],
            self.robot_pos[1] + self.dirs[self.dir][0][1],
        )

    def run_program_paint(self):
        while True:
            colour = self.painted_panels.get(self.robot_pos, 0)
            self.brain.updateInput(colour)

            output, end = self.brain.run_program()

            self.output_nums.append(output)

            if len(self.output_nums) >= 2:
                paint_num = self.output_nums.pop(0)
                self.painted_panels[self.robot_pos] = paint_num

                dir_num = self.output_nums.pop(0)
                if dir_num == 0:
                    self.dir = self.dirs[self.dir][1]
                else:
                    self.dir = self.dirs[self.dir][2]

                self.moveForward()

            if end == 99:
                break

        return len(self.painted_panels)


def part1(data):
    robot = Robot(data, 0)
    ans = robot.run_program_paint()
    return ans


def part2(data):
    robot = Robot(data, 1)
    robot.painted_panels = {(0, 0): 1}
    robot.run_program_paint()
    keys = list(robot.painted_panels.keys())
    x_values = [item[0] for item in keys]
    y_values = [item[1] for item in keys]
    max_y = max(y_values)
    min_y = min(y_values)
    max_x = max(x_values)
    min_x = min(x_values)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            colour = robot.painted_panels.get((x, y), 0)
            if colour == 0:
                print(" ", end="")
            else:
                print("#", end="")
        print()
