from intcode import IntcodeComputer


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
