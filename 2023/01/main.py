import re

from functools import reduce

from util import reverse_str, dprint


# Assumes there is always at lease one digit per calibration_line
def parse_calibration_value_1(calibration_line: str):
    start_digit = ""
    end_digit = ""
    for char in calibration_line:
        if char.isdigit():
            if start_digit == "":
                start_digit = char
            end_digit = char
    return int(start_digit + end_digit)


first_digit_regex = re.compile("([0-9]|one|two|three|four|five|six|seven|eight|nine)")
last_digit_regex = re.compile("([0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)")
conjoined_digit_regex = re.compile("(oneight|twone|threeight|nineight|sevenine|fiveight)")
digit_regex = re.compile("[0-9]")
word_to_digit = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


# This one can't handle conjoined digits for the last digit,
# for example: 1fiveight should return 18, but it returns 15
def parse_calibration_value_2_bad(calibration_line: str):
    found_digits = first_digit_regex.findall(calibration_line)
    start_digit = found_digits[0] if len(found_digits[0]) == 1 else word_to_digit[found_digits[0]]
    assert digit_regex.match(start_digit), f"{calibration_line} start digit not a digit: {start_digit}"
    end_digit = found_digits[-1] if len(found_digits[-1]) == 1 else word_to_digit[found_digits[-1]]
    assert digit_regex.match(end_digit), f"{calibration_line} end digit not a digit: {end_digit}"

    dprint(f"{calibration_line}")
    dprint(f"found digits: {found_digits}")
    dprint(f"raw start: {found_digits[0]} end: {found_digits[-1]}")
    dprint(f"int start: {start_digit} end: {end_digit}\n")

    result = int(start_digit + end_digit)

    return result


def parse_calibration_value_2(calibration_line: str):
    first_digit_raw = first_digit_regex.search(calibration_line).group()
    last_digit_raw = reverse_str(last_digit_regex.search(reverse_str(calibration_line)).group())
    start_digit = first_digit_raw if len(first_digit_raw) == 1 else word_to_digit[first_digit_raw]
    end_digit = last_digit_raw if len(last_digit_raw) == 1 else word_to_digit[last_digit_raw]
    return int(start_digit + end_digit)


def calculate_calibration(parse_method, calibration_text: str):
    lines = calibration_text.splitlines()
    calibration_values = map(parse_method, lines)
    dprint(f"found {len(lines)} entries")
    return reduce(lambda l, r: l + r, calibration_values)


def print_calibration(path, short=False):
    print(f"reading file {path}")
    with open(path, encoding="utf-8") as file:
        text = file.read()
        if short:
            text = "".join(text.splitlines(keepends=True)[0:5])
        print(f'calibration value level 1: {calculate_calibration(parse_calibration_value_1, text)}')
        # print(f'calibration value level 2 old: {calculate_calibration(parse_calibration_value_2_bad, text)}')
        print(f'calibration value level 2: {calculate_calibration(parse_calibration_value_2, text)}')
    print("done with file.")


if __name__ == "__main__":
    print_calibration("./puzzle-data")
