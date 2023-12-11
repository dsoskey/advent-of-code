import re

number_regex = re.compile(r"\d+")
symbol_regex = re.compile(r"[^.0-9]")
star_regex = re.compile(r"\*")


# Assumes schematics are rectangular, aka each row has the same length
class Schematic:
    def __init__(self, raw_text: str):
        grid = raw_text.splitlines(False)
        self.width = len(grid[0])
        self.height = len(grid)
        self.raw_text = "".join(grid)
        self.num_lookup = dict()
        for i in range(0, len(grid)):
            line = grid[i]
            for match in number_regex.finditer(line):
                for index in range(match.start(), match.end()):
                    offset = i * self.width
                    self.num_lookup[index + offset] = \
                        dict(group=match.group(), range=range(match.start() + offset, match.end() + offset))

    def coordinates(self, index: int):
        return index % self.width, int(index / self.width)

    @staticmethod
    def left(index: int):
        return index - 1

    @staticmethod
    def right(index: int):
        return index + 1

    def up(self, index: int):
        return index - self.width

    def down(self, index: int):
        return index + self.width

    def around_me(self, i: int):
        return f"{self.raw_text[self.up(self.left(i))]}{self.raw_text[self.up(i)]}{self.raw_text[self.up(self.right(i))]}\n" + \
            f"{self.raw_text[self.left(i)]}{self.raw_text[i]}{self.raw_text[self.right(i)]}\n" + \
            f"{self.raw_text[self.down(self.left(i))]}{self.raw_text[self.down(i)]}{self.raw_text[self.down(self.right(i))]}\n"

    def neighbors(self, index: int):
        x, y = self.coordinates(index)
        left_edge = x > 0
        right_edge = x < self.width - 1
        top_edge = y != 0
        bottom_edge = y != self.height - 1
        result = set()
        if left_edge:
            result.add(self.left(index))
            if top_edge:
                result.add(self.up(self.left(index)))
            if bottom_edge:
                result.add(self.down(self.left(index)))
        if right_edge:
            result.add(self.right(index))
            if top_edge:
                result.add(self.up(self.right(index)))
            if bottom_edge:
                result.add(self.down(self.right(index)))
        if top_edge:
            result.add(self.up(index))
        if bottom_edge:
            result.add(self.down(index))
        return result

    def visit_symbols_1(self):
        used_indices = set()
        to_add = []
        for symbol in symbol_regex.finditer(self.raw_text):
            symbol_index = symbol.start()
            for neighbor in self.neighbors(symbol_index):
                if neighbor not in used_indices:
                    match = self.num_lookup.get(neighbor)
                    if match is not None:
                        to_add.append(int(match.get("group")))
                        for index in match.get("range"):
                            used_indices.add(index)
        return sum(to_add)

    def visit_symbols_2(self):
        to_add = []
        for symbol in symbol_regex.finditer(self.raw_text):
            i = symbol.start()
            neighbor_numbers = []
            used_indices = set()
            for neighbor in self.neighbors(i):
                if neighbor not in used_indices:
                    match = self.num_lookup.get(neighbor)
                    if match is not None:
                        neighbor_numbers.append(int(match.get("group")))
                        for index in match.get("range"):
                            used_indices.add(index)
            if len(neighbor_numbers) == 2:
                to_add.append(neighbor_numbers[0] * neighbor_numbers[1])
        return sum(to_add)


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        s = Schematic(text)
        print(f"star 1: {s.visit_symbols_1()}")
        print(f"star 2: {s.visit_symbols_2()}")
