from functools import reduce


def differences(nums):
    return [(nums[i + 1] - nums[i]) for i in range(len(nums) - 1)]


def generate_difference_matrix(nums):
    result = [nums]
    current = nums
    while any(current):
        current = differences(current)
        result.append(current)
    return result


def extrapolate(nums):
    diff_matrix = generate_difference_matrix(nums)
    result = sum(map(lambda line: line[-1], diff_matrix))
    return result


def reverse_extrapolate(nums):
    diff_matrix = generate_difference_matrix(nums)
    diff_matrix.reverse()
    result = reduce(lambda curr, n_xt: n_xt - curr, map(lambda line: line[0], diff_matrix))
    return result


def parse_history_matrix(raw_text: str):
    lines = raw_text.splitlines()
    return list(map(lambda line: list(map(int, line.split(" "))), lines))


if __name__ == "__main__":
    with open("./input") as file:
        history_matrix = parse_history_matrix(file.read())
        print(f"extrapolated sum: {sum(map(extrapolate, history_matrix))}")
        print(f"prextrapolated sum: {sum(map(reverse_extrapolate, history_matrix))}")
