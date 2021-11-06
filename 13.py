from intcode import IntcodeComputer


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
