import re
from functools import reduce


def num_record_options(race_time: int, record_dist: int):
    return len(list(filter(
        lambda it: it > record_dist,
        map(lambda speed: (race_time - speed) * speed, range(race_time + 1))
    )))


def multi_number_of_record_options(raw_race: str):
    time_raw, dist_raw = raw_race.splitlines()
    times = list(map(int, re.split(r"\s+", time_raw)[1:]))
    dists = list(map(int, re.split(r"\s+", dist_raw)[1:]))
    return reduce(
        int.__mul__,
        map(lambda t: num_record_options(*t), zip(times, dists))
    )


def multi_number_of_record_options(raw_race: str):
    time_raw, dist_raw = raw_race.splitlines()
    times = list(map(int, re.split(r"\s+", time_raw)[1:]))
    dists = list(map(int, re.split(r"\s+", dist_raw)[1:]))
    return reduce(
        int.__mul__,
        map(lambda t: num_record_options(*t), zip(times, dists))
    )


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        print(f"multiplied wins: {multi_number_of_record_options(text)}")
        print(f"multiplied wins: {multi_number_of_record_options(text)}")
