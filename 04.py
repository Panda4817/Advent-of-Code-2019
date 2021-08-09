def password_meet_criteria(n):
    criteria_matched = 2  # within range and 6 digits assumed
    digits = [int(i) for i in list(str(n))]
    for d, i in zip(digits, range(5)):
        if (
            i > 0
            and i < 4
            and d == digits[i + 1]
            and d != digits[i - 1]
            and d != digits[i + 2]
        ):
            criteria_matched += 1
            break
        elif i == 0 and d == digits[i + 1] and d != digits[i + 2]:
            criteria_matched += 1
            break
        elif i == 4 and d == digits[i + 1] and d != digits[i - 1]:
            criteria_matched += 1
            break

    for d, i in zip(digits, range(5)):
        if d > digits[i + 1]:
            break
    else:
        criteria_matched += 1

    if criteria_matched == 4:
        return True

    return False


def part1(data):
    low, high = (int(i) for i in data.split("-"))
    total_possible = 0
    for n in range(low + 1, high):
        if password_meet_criteria(n):
            total_possible += 1

    return total_possible
