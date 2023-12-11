import re


def parse_ticket(raw_game: str):
    header, numbers = raw_game.split(": ")
    raw_wins, raw_nums = numbers.split(" | ")
    wins = set(map(lambda it: int(it), re.split(r"\s+", raw_wins.strip())))
    nums = set(map(lambda it: int(it), re.split(r"\s+", raw_nums.strip())))
    return int(re.split(r"\s+", header)[-1]), len(wins.intersection(nums))


def points_won(raw_game: str):
    _, overlap = parse_ticket(raw_game)
    return 2 ** (overlap - 1) if overlap > 0 else 0


def cards_won(raw_games):
    games = list(map(parse_ticket, raw_games))
    to_process = dict()
    result = 0
    for index in range(0, len(games)):
        game_id, overlap = games[index]
        num_copies = 1 + to_process.get(game_id, 0)
        result += num_copies
        for next_id in range(game_id + 1, game_id + overlap + 1):
            if to_process.get(next_id) is None:
                to_process[next_id] = 0
            to_process[next_id] += num_copies
    return result


if __name__ == "__main__":
    with open("./input") as file:
        raw_games = file.read().splitlines(False)
        print(f"total points {sum(map(points_won, raw_games))}")  # 18519
        print(f"cards won {cards_won(raw_games)}")  # 11787590
