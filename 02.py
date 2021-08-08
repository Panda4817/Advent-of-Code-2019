def run_program(numbers, val1, val2):
    numbers[1] = val1
    numbers[2] = val2
    length = len(numbers)

    for i in range(0, length - 4, 4):
        if numbers[i] == 99:
            break

        pos1 = numbers[i + 1]
        pos2 = numbers[i + 2]
        pos3 = numbers[i + 3]

        output = 0
        if numbers[i] == 1:
            output = numbers[pos1] + numbers[pos2]
        elif numbers[i] == 2:
            output = numbers[pos1] * numbers[pos2]

        numbers[pos3] = output

    return numbers[0]


def part1(data):
    numbers = [int(i) for i in data.split(",")]
    return run_program(numbers, 12, 2)


def part2(data):
    goal = 19690720
    val1 = 0
    val2 = 0

    while True:
        numbers_list = [int(i) for i in data.split(",")]
        output = run_program(numbers_list, val1, val2)
        if output == goal:
            break

        val2 += 1
        if val2 == 100:
            val1 += 1
            val2 = 0

        if val1 == 100:
            break

    return (100 * val1) + val2
