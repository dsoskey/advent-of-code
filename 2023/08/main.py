from functools import reduce
from math import lcm


def parse_node(raw_text: str):
    source, raw_dest = raw_text.split(" = ")
    left, right = raw_dest[1:-1].split(', ')
    return dict(src=source, L=left, R=right)


def collect(prev, _next):
    prev[_next["src"]] = _next
    return prev


def parse_map(raw_text: str):
    steps, raw_nodes = raw_text.split("\n\n")
    nodes = map(parse_node, raw_nodes.splitlines())
    node_map = reduce(collect, nodes, {})
    return steps, node_map


def num_steps(raw_text: str, start: str, target: str):
    steps, node_map = parse_map(raw_text)
    result = 0
    step_index = 0
    current_node = node_map[start]
    while current_node["src"] != target:
        direction = steps[step_index]
        current_node = node_map[current_node[direction]]
        result += 1
        if step_index < len(steps) - 1:
            step_index += 1
        else:
            step_index = 0
    return result


def has_last_char(char: str):
    def inner(it):
        return it["src"][-1] == char

    return inner


def num_simul_steps(raw_text: str, start_char: str, target_char: str):
    steps, node_map = parse_map(raw_text)
    result = 0
    step_index = 0
    current_nodes = list(filter(has_last_char(start_char), node_map.values()))
    multiples = list(map(lambda n: 0, current_nodes))
    while not all(map(lambda it: it > 0, multiples)):
        direction = steps[step_index]
        new_nodes = []
        for i, node in enumerate(current_nodes):
            new_node = node_map[node[direction]]
            new_nodes.append(new_node)
            if new_node["src"][-1] == target_char:
                if multiples[i] == 0:
                    multiples[i] = -1 * result
                elif multiples[i] < 0:
                    multiples[i] = result - (-1 * multiples[i])
        current_nodes = new_nodes
        result += 1
        if step_index < len(steps) - 1:
            step_index += 1
        else:
            step_index = 0
    return lcm(*multiples)


if __name__ == "__main__":
    with open("./input") as file:
        text = file.read()
        start = "AAA"
        end = "ZZZ"
        print(f"steps from {start} to {end}: {num_steps(text, start, end)}")
        print(f"ghost steps from {start[-1]} to {end[-1]}: {num_simul_steps(text, start[-1], end[-1])}")