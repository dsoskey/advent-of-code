from copy import deepcopy
from functools import reduce


def index_of(condition, _list):
    for i in range(len(_list)):
        if condition(_list[i]):
            return i
    return -1


class RangeMap:
    def __init__(self, raw_map: str):
        name, _map = raw_map.split(" map:\n")
        self.src, self.dst = name.split("-to-")
        self.by_src = sorted(map(RangeMap.parse_wee, _map.splitlines()), key=lambda it: it["src_range"].start)
        self.by_dst = sorted(map(RangeMap.parse_wee, _map.splitlines()), key=lambda it: it["dst_range"].start)
        self.ranges = list(map(RangeMap.parse_map_line, _map.splitlines()))

    @staticmethod
    def parse_map_line(raw_line: str):
        destination, source, _range = \
            map(lambda i: int(i), raw_line.split(" "))

        input_range = range(source, source + _range)
        return dict(dst_start=destination, input_range=input_range)

    @staticmethod
    def parse_wee(raw_line: str):
        destination, source, _range = \
            map(lambda i: int(i), raw_line.split(" "))
        return dict(
            src_range=range(source, source + _range),
            dst_range=range(destination, destination + _range),
            to_add=destination - source,
        )

    def other_parse(self, line: str):
        destination, source, _range = \
            map(lambda i: int(i), line.split(" "))
        return source, destination, _range

    def merge_ranges(self, other):
        print(f"merge target {other.dst}")
        new_ranges = []
        for self_range in self.by_dst:
            # get subset of other ranges that self_range's dst_range fits in
            # split self_range into new ranges by those other ranges
            src_range = self_range["src_range"]
            dst_range = self_range["dst_range"]
            to_add = self_range["to_add"]
            start_index = index_of(lambda r: dst_range.start in r["src_range"], other.by_src)
            end_index = index_of(lambda r: dst_range.stop - 1 in r["src_range"], other.by_src)
            # missed edge case? dst_range.start isn't in any of other.by_src["src_range"] but dst_range.stop is in a range
            if start_index == -1 and end_index > -1:
                print(dst_range)
                print(other.by_src[end_index-1])
                print(other.by_src[end_index])
            if start_index == -1 and end_index == -1:
                # it wasn't found in any of other's src_ranges, we should add self_range to new_ranges unchanged
                first_match = index_of(lambda r: dst_range.start > r["src_range"].start, other.by_src)
                # if first_match > 0:
                new_ranges.append(self_range)
            else:
                # look for a range that contains end
                # if no matching range, find the first range that's bigger
                next_bigger = index_of(lambda r: dst_range.stop < r["src_range"].start, other.by_src)
                end_index = (next_bigger if next_bigger == -1 else next_bigger - 1) \
                    if end_index == -1 \
                    else end_index
                to_split = other.by_src[start_index:]\
                    if end_index == -1\
                    else other.by_src[start_index:end_index + 1]
                new_src_end = src_range.start
                for sub_range in to_split:
                    new_dst_start = dst_range.start + sub_range["to_add"] \
                        if dst_range.start in sub_range["src_range"]\
                        else sub_range["dst_range"].start
                    new_dst_end = dst_range.stop + sub_range["to_add"]\
                        if dst_range.stop in sub_range["src_range"] \
                        else sub_range["dst_range"].stop
                    new_range_size = new_dst_end - new_dst_start
                    assert new_range_size <= dst_range.stop - dst_range.start, "split range cant be bigger than subrange"
                    new_src_start = new_dst_start - to_add - sub_range["to_add"]
                    new_src_end = new_src_start + new_range_size
                    new_ranges.append(dict(
                        src_range=range(new_src_start, new_src_end),
                        dst_range=range(new_dst_start, new_dst_end),
                        to_add=to_add + sub_range["to_add"]
                    ))
                # means there was some leftover
                if end_index == -1:
                    new_ranges.append(dict(
                        src_range=range(new_src_end, src_range.stop),
                        dst_range=range(new_src_end + to_add, src_range.stop + to_add),
                        to_add=to_add
                    ))
        self.by_src = sorted(new_ranges, key=lambda it: it["src_range"].start)
        self.by_dst = sorted(new_ranges, key=lambda it: it["dst_range"].start)
        self.dst = other.dst
        return self

    def get(self, value: int):
        for _range in self.ranges:
            dst_start = _range["dst_start"]
            input_range = _range["input_range"]
            if value in input_range:
                offset = value - input_range.start
                return dst_start + offset
        return value

    def output_range(self):
        return range(
            self.by_dst[0]["dst_range"].start,
            self.by_dst[-1]["dst_range"].stop,
        )


def collect(_object, _next: RangeMap):
    _object[_next.src] = _next
    return _object


def parse_seeds_v1(raw_seeds: str):
    return map(lambda i: int(i), raw_seeds.replace("seeds: ", "").split(" "))


def parse_seeds_v2(raw_seeds: str):
    numbers = list(map(lambda it: int(it), raw_seeds.replace("seeds: ", "").split(" ")))
    result = []
    for i in range(0, len(numbers), 2):
        start, offset = numbers[i:i + 2]
        result.append(range(start, start + offset))
    return result


def lowest_location_v1(parse_seeds, raw_almanac: str):
    splitted = raw_almanac.split("\n\n")
    maps = map(lambda it: RangeMap(it), splitted[1:])
    mom = reduce(collect, maps, dict())
    locations = []
    for seed in parse_seeds(splitted[0]):
        target = "seed"
        result = seed
        while target != "location":
            current_map = mom[target]
            result = current_map.get(result)
            target = current_map.dst
        locations.append(result)
    return min(locations)


def lowest_location_v2(raw_almanac: str):
    splitted = raw_almanac.split("\n\n")
    seed_ranges = parse_seeds_v2(splitted[0])
    mom = reduce(collect, map(lambda it: RangeMap(it), splitted[1:]), dict())
    _combined: RangeMap = deepcopy(mom["seed"])
    while _combined.dst != "location":
        _prev = mom[_combined.src]
        _next = mom[_combined.dst]
        _combined = _combined.merge_ranges(_next)
    outputs = []
    for input_range in seed_ranges:
        last_start = input_range.start
        appended = False
        for target_range in _combined.by_src:
            if last_start in target_range["src_range"]:
                outputs.append(last_start + target_range["to_add"])
                appended = True
                last_start = min([target_range["src_range"].stop, input_range.stop])
        if not appended:
            # not found in a src range, so add it with no changes
            outputs.append(input_range.start)

    return min(outputs)


if __name__ == "__main__":
    with open("./input") as file:
        almanac = file.read()
        print(f"lowest location 1: {lowest_location_v1(parse_seeds_v1, almanac)}")
        print(f"lowest location 2: {lowest_location_v2(almanac)}")

# 37405178 is too high
# 10834440