import copy


def process_data(data):
    numbers = [int(x) for x in list(data)]
    return numbers


def run_fft(numbers, total):
    pattern = [0, 1, 0, -1]
    i = 0
    length = len(numbers)
    while i < total:
        temp = []
        for p in range(length):

            temp_total = 0

            pi = 0
            pj = 0
            for n in numbers:
                pj += 1
                if pj > p:
                    pi += 1
                    if pi > 3:
                        pi = 0
                    pj = 0
                temp_total += n * pattern[pi]

            temp.append(int(str(temp_total)[-1]))
        numbers = temp

        i += 1

    return numbers


def part1(data):
    numbers = process_data(data)
    numbers = run_fft(numbers, 100)
    return numbers[0:8]


def part2(data):
    numbers = process_data(data)
    signal = []
    for i in range(10000):
        signal.extend(numbers)
    message_offset = signal[0:7]
    signal = run_fft(signal, 100)
    return numbers[message_offset : message_offset + 8]
