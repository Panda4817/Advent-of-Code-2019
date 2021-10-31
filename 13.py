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


class Arcade:
    def __init__(self, data, input) -> None:
        self.brain = IntcodeComputer(data, input)
        self.tiles = {}
        self.output_nums = []
        self.segment_display = 0
        self.ball = None
        self.paddle = None

    def run_arcade_program(self):
        while True:
            output, end = self.brain.run_program()

            self.output_nums.append(output)

            if len(self.output_nums) >= 3:
                x = self.output_nums.pop(0)
                y = self.output_nums.pop(0)
                tile_id = self.output_nums.pop(0)
                if x == -1 and y == 0:
                    self.segment_display = tile_id
                else:
                    self.tiles[(x, y)] = tile_id
                    if tile_id == 3:
                        self.paddle = (x, y)
                    elif tile_id == 4:
                        self.ball = (x, y)

            if self.ball != None and self.paddle != None:
                if self.ball[0] < self.paddle[0]:
                    self.brain.updateInput(-1)
                elif self.ball[0] > self.paddle[0]:
                    self.brain.updateInput(1)
                else:
                    self.brain.updateInput(0)

            if end == 99:
                break

    def print_board(self):
        keys = list(self.tiles.keys())
        x_values = [item[0] for item in keys]
        y_values = [item[1] for item in keys]
        max_y = max(y_values)
        min_y = min(y_values)
        max_x = max(x_values)
        min_x = min(x_values)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                type = self.tiles.get((x, y), 0)
                if type == 0:
                    print("  ", end="")
                elif type == 1:
                    print("##", end="")
                elif type == 2:
                    print("[]", end="")
                elif type == 3:
                    print("--", end="")
                else:
                    print("()", end="")
            print()


def part1(data):
    arcade = Arcade(data, 0)
    arcade.run_arcade_program()
    arcade.print_board()
    block_tiles = 0
    for k, v in arcade.tiles.items():
        if v == 2:
            block_tiles += 1

    return block_tiles


def part2(data):
    arcade = Arcade(data, 0)
    arcade.brain.numbers[0] = 2
    arcade.run_arcade_program()
    return arcade.segment_display
