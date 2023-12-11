from itertools import combinations

empty_space = "."
galaxy = "#"


def expand_map(raw_txt: str):
    y_adds = []
    splitted = raw_txt.splitlines(False)
    for y in range(len(splitted)):
        row = splitted[y]
        if all(map(lambda char: char == empty_space, row)):
            y_adds.append(y)
    x_adds = []
    for x in range(len(splitted[0])):
        if all(map(lambda row: row[x] == empty_space, splitted)):
            x_adds.append(x)
    return x_adds, y_adds


class GalaxyExpansionMap:
    def __init__(self, raw_txt: str):
        self.raw_txt = raw_txt
        self.grid = raw_txt.splitlines(False)
        self.empty_x, self.empty_y = expand_map(raw_txt)

    def galaxy_coordinates(self):
        result = []
        for y in range(len(self.grid)):
            row = self.grid[y]
            for x in range(len(row)):
                if row[x] == galaxy:
                    result.append((x, y))
        return result

    def galaxy_shortest_path(self, expansion_factor):
        coords = self.galaxy_coordinates()
        # accounts for initial empty space
        expansion = expansion_factor - 1

        def distance_function(pair):
            left, right = pair
            lx, ly = left
            rx, ry = right

            expansion_x = len(list(filter(lambda it: it in range(min([lx, rx]), max([lx, rx])), self.empty_x)))
            expansion_y = len(list(filter(lambda it: it in range(min([ly, ry]), max([ly, ry])), self.empty_y)))

            x_component = abs(lx - rx) + expansion * expansion_x
            y_component = abs(ly - ry) + expansion * expansion_y
            return x_component + y_component

        comb = combinations(coords, 2)
        return sum(map(distance_function, comb))


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        mapa = GalaxyExpansionMap(text)
        print(f"shortest value double expansion {mapa.galaxy_shortest_path(2)}")
        print(f"shortest value 1 mill expansion {mapa.galaxy_shortest_path(1000000)}")
