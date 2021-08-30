from typing import List
import itertools


class IntcodeComputer:
    def __init__(self, data, input: List) -> None:
        self.input = input
        self.numbers = [int(i) for i in data.split(",")]
        self.final_output = 0
        self.pointer = 0

    def save_input(self, a, b, c):
        self.numbers[c] = self.input.pop(0)
        return 2

    def get_output(self, a, b, c):
        self.final_output = c
        # print(self.final_output)
        return 2

    def add(self, a, b, c):
        self.numbers[c] = a + b
        return 4

    def multiply(self, a, b, c):
        self.numbers[c] = a * b
        return 4

    def jump_if_true(self, a, b, c):
        if a != 0:
            return b - c
        return 3

    def jump_if_false(self, a, b, c):
        if a == 0:
            return b - c
        return 3

    def less_than(self, a, b, c):
        if a < b:
            self.numbers[c] = 1
        else:
            self.numbers[c] = 0
        return 4

    def equals(self, a, b, c):
        if a == b:
            self.numbers[c] = 1
        else:
            self.numbers[c] = 0
        return 4

    def unknown(self, a, b, c):
        return 1

    def identify_mode(self, mode, pointer):
        if mode == 0:
            pos = self.numbers[pointer]
            param = self.numbers[pos]
        else:
            param = self.numbers[pointer]
        return param

    def identify_parameters(self, current_pos):
        modes = [int(i) for i in list(str(self.numbers[current_pos]))]
        while len(modes) < 5:
            modes.insert(0, 0)
        # a, b, c are the parameters, not all opcodes have 3 params
        if modes[-1] == 1:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.numbers[current_pos + 3]
            func = self.add
        elif modes[-1] == 2:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.numbers[current_pos + 3]
            func = self.multiply
        elif modes[-1] == 3:
            a = None
            b = None
            c = self.numbers[current_pos + 1]
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
            c = self.numbers[current_pos + 3]
            func = self.less_than
        elif modes[-1] == 8:
            a = self.identify_mode(modes[2], current_pos + 1)
            b = self.identify_mode(modes[1], current_pos + 2)
            c = self.numbers[current_pos + 3]
            func = self.equals
        else:
            # Should never reach if no errors
            a = None
            b = None
            c = None
            func = self.unknown

        # print(modes, current_pos, a, b, c, func.__name__)
        return a, b, c, func

    def run_program(self):
        while True:
            a, b, c, func = self.identify_parameters(self.pointer)
            jump = func(a, b, c)

            self.pointer += jump
            if self.numbers[self.pointer] == 99 or func.__name__ == "get_output":
                break

        return self.final_output, self.numbers[self.pointer]


def part1(data):
    phase_settings = list(itertools.permutations([0, 1, 2, 3, 4]))
    max_thruster = 0
    chosen_combo = None
    for phase_setting in phase_settings:
        input_signal = 0
        for phase in phase_setting:
            start_input = [phase, input_signal]
            computer = IntcodeComputer(data, start_input)
            input_signal, halt = computer.run_program()
        if input_signal > max_thruster:
            max_thruster = input_signal
            chosen_combo = phase_setting

    return max_thruster, chosen_combo


def part2(data):
    feedback_phase_settings = list(itertools.permutations([5, 6, 7, 8, 9]))
    max_thruster = 0
    chosen_combo = None

    for feedback_mode_phases in feedback_phase_settings:
        input_signal = 0
        index = 0
        amplifiers = [IntcodeComputer(data, [])]
        halt = 0
        for phase in feedback_mode_phases:
            if len(amplifiers) < (index + 1):
                amplifiers.append(IntcodeComputer(data, []))
            amplifiers[index].input.append(phase)
            amplifiers[index].input.append(input_signal)
            input_signal, halt = amplifiers[index].run_program()
            index += 1

        index = 0
        while True:
            amplifiers[index].input.append(input_signal)
            input_signal, halt = amplifiers[index].run_program()
            index += 1

            if halt == 99 and index == 5:
                break

            if index == 5:
                index = 0

        if input_signal > max_thruster:
            max_thruster = input_signal
            chosen_combo = feedback_mode_phases

    return max_thruster, chosen_combo
