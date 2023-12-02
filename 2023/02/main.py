import re
from functools import reduce


# 0 means it wasn't valid. anything else is valid and indicates the game id
def game_value_1(game_str, rgb: dict):
    coloned = game_str.split(": ")
    games = coloned[1].split("; ")

    for game in games:
        draws = game.split(", ")
        for draw in draws:
            split = draw.split(" ")
            color = split[1]
            amount = int(split[0])
            if amount > rgb.get(color, 0):
                return 0
    return int(coloned[0].split(" ")[1])


def total_value_1(games_str: str, rgb: dict):
    mapped = map(lambda g: game_value_1(g, rgb), games_str.splitlines())
    return reduce(lambda l, r: l + r, mapped)


regex = re.compile(r'\d+ (red|blue|green)')


def game_value_2(game_str):
    coloned = game_str.split(": ")
    rgb = dict(red=0, green=0, blue=0)
    for match in regex.finditer(coloned[1]):
        ramt, color = match.group().split(" ")
        amount = int(ramt)
        if amount > rgb.get(color, 0):
            rgb[color] = amount
    return reduce(lambda l, r: l * r, rgb.values())


def total_value_2(games_str: str):
    mapped = map(game_value_2, games_str.splitlines())
    return reduce(lambda l, r: l + r, mapped)


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        print(total_value_1(text, dict(blue=14, red=12, green=13)))
        print(total_value_2(text))
