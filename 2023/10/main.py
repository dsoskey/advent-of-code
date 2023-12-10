import re
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


class PipeMap:
    valid_connections = {
        "|": {"N", "S"},
        "-": {"E", "W"},
        "L": {"N", "E"},
        "J": {"N", "W"},
        "7": {"S", "W"},
        "F": {"S", "E"},
        ".": set(),
        "S": {"!"},
    }
    to_pipe = {
        "|": "║",
        "-": "═",
        "L": "╚",
        "J": "╝",
        "7": "╗",
        "F": "╔",
        ".": ".",
        "S": "S",
    }

    def __init__(self, raw_text: str):
        self.grid = raw_text.splitlines(False)
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def start_coord(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.char_at(x, y) == "S":
                    return x, y

    def char_at(self, x, y):
        return self.grid[y][x]

    def pipe_neighbors(self, coord: tuple):
        x, y = coord
        char = self.char_at(x, y)
        w_edge = x > 0 and len({"W", "!"} & PipeMap.valid_connections[char])
        e_edge = x < self.width - 1 and len({"E", "!"} & PipeMap.valid_connections[char])
        n_edge = y != 0 and len({"N", "!"} & PipeMap.valid_connections[char])
        s_edge = y != self.height - 1 and len({"S", "!"} & PipeMap.valid_connections[char])
        result = set()
        if w_edge:
            connections = PipeMap.valid_connections[self.char_at(x - 1, y)]
            if len({"!", "E"} & connections):
                result.add((x - 1, y))
        if e_edge:
            connections = PipeMap.valid_connections[self.char_at(x + 1, y)]
            if len({"!", "W"} & connections):
                result.add((x + 1, y))
        if n_edge:
            connections = PipeMap.valid_connections[self.char_at(x, y - 1)]
            if len({"!", "S"} & connections):
                result.add((x, y - 1))
        if s_edge:
            connections = PipeMap.valid_connections[self.char_at(x, y + 1)]
            if len({"!", "N"} & connections):
                result.add((x, y + 1))
        return result

    def gap_neighbors(self, coord: tuple, pipes):
        x, y = coord
        w_edge = x > 0
        e_edge = x < self.width - 1
        n_edge = y != 0
        s_edge = y != self.height - 1
        result = set()
        if w_edge and (x - .5, y) not in pipes:
            result.add((x - .5, y))
        if e_edge and (x + .5, y) not in pipes:
            result.add((x + .5, y))
        if n_edge and (x, y - .5) not in pipes:
            result.add((x, y - .5))
        if s_edge and (x, y + .5) not in pipes:
            result.add((x, y + .5))
        return result

    def is_edge(self, coord: tuple):
        x, y = coord
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def furthest_distance(self):
        start = self.start_coord()
        neighbors = self.pipe_neighbors(start)
        current = neighbors.pop()
        steps = 1
        visited = {current}
        connection_1 = (
            current[0] if start[0] == current[0] else min(current[0], start[0]) + .5,
            current[1] if start[1] == current[1] else min(current[1], start[1]) + .5,
        )
        connections = {connection_1}
        while self.char_at(current[0], current[1]) != "S":
            neighbors = self.pipe_neighbors(current)
            to_check = visited if steps > 1 else visited.union({start})
            next_pipe = neighbors.difference(to_check).pop()
            connection = (
                current[0] if next_pipe[0] == current[0] else min(current[0], next_pipe[0]) + .5,
                current[1] if next_pipe[1] == current[1] else min(current[1], next_pipe[1]) + .5,
            )
            connections.add(connection)
            current = next_pipe
            visited.add(current)
            steps += 1
        return steps / 2, visited.union({start}), connections

    def enclosed_area(self):
        steps, visited, connections = self.furthest_distance()
        pipes = visited.union(connections)
        l = list(map(lambda x: [(x, y) for y in range(self.height)], range(self.width)))
        all_coords = set([item for sublist in l for item in sublist])

        junk_tiles = all_coords.difference(visited).difference(connections)
        to_visit = set(filter(lambda it: self.is_edge(it), junk_tiles))
        visited_junk = set()
        while len(to_visit):
            current = to_visit.pop()
            visited_junk.add(current)
            neighbors = self.gap_neighbors(current, pipes)
            for n in neighbors:
                if n not in visited_junk:
                    to_visit.add(n)
        result = junk_tiles.difference(visited_junk)
        # self.highlight_coords(visited)
        # self.highlight_with_gaps(visited, connections)
        self.highlight_with_gap_unreachables(visited, connections, visited_junk, result)
        # self.highlight_with_unreachables(visited, visited_junk, result)
        return len(result)

    def highlight_coords(self, coord_set):
        for y in range(len(self.grid)):
            row = [(PipeMap.to_pipe[self.char_at(x, y)] if (x, y) in coord_set else "0") for x in
                   range(len(self.grid[y]))]
            print("".join(row))

    def highlight_with_gaps(self, coord_set, connections):
        for y in range(len(self.grid)):
            row = []
            gap = []
            for x in range(len(self.grid[y])):
                row.append(PipeMap.to_pipe[self.char_at(x, y)] if (x, y) in coord_set else "0")
                row.append("─" if (x + .5, y) in connections else " ")
                gap.append("│" if (x, y + .5) in connections else " ")
                gap.append(" ")
            print("".join(row))
            print("".join(gap))

    def highlight_with_unreachables(self, coord_set, visited_junk, unreachable_gaps):
        for y in range(len(self.grid)):
            row = []
            gap = []
            for x in range(len(self.grid[y])):
                if (x, y) in coord_set:
                    row.append(PipeMap.to_pipe[self.char_at(x, y)])
                elif (x, y) in unreachable_gaps:
                    row.append("1")
                elif (x, y) in visited_junk:
                    row.append("▒")
                else:
                    row.append(" ")
            print("".join(row))

    def highlight_with_gap_unreachables(self, coord_set, connections, visited_junk, unreachable_gaps):
        for y in range(len(self.grid)):
            row = []
            gap = []
            for x in range(len(self.grid[y])):
                if (x, y) in coord_set:
                    row.append(PipeMap.to_pipe[self.char_at(x, y)])
                elif (x, y) in unreachable_gaps:
                    row.append("1")
                elif (x, y) in visited_junk:
                    row.append("▒")
                else:
                    row.append(" ")

                if (x + .5, y) in connections:
                    row.append("─")
                elif (x + .5, y) in visited_junk:
                    row.append("▒")
                else:
                    row.append(" ")

                if (x, y + .5) in connections:
                    gap.append("│")
                elif (x, y + .5) in visited_junk:
                    gap.append("▒")
                else:
                    gap.append(" ")

                if (x + .5, y + .5) in visited_junk:
                    gap.append("▒")
                else:
                    gap.append(" ")
            print("".join(row))
            print("".join(gap))


if __name__ == "__main__":
    with open("./sample-0") as file:
        text = file.read()
        pipe_map = PipeMap(text)
        # print(f"furthest distance {pipe_map.furthest_distance()[0]}")
        print(f"num enclosed {pipe_map.enclosed_area()}")
