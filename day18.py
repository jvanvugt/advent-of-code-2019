import string

from dataclasses import dataclass
from typing import Tuple, FrozenSet, NamedTuple
from collections import deque, defaultdict
from utils import neighbours
import heapq


KEYS = set(string.ascii_lowercase)
DOORS = set(string.ascii_uppercase)


def find_start_pos(world):
    starts = []
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col] == "@":
                starts.append((row, col))
    return tuple(starts)


def find_num_keys(world):
    keys = 0
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col] in KEYS:
                keys += 1
    return keys


@dataclass
class State:
    pos: Tuple[int, int]
    keys: FrozenSet[set]
    num_steps: int


def a(world):
    def w(pos):
        return world[pos[0]][pos[1]]

    start_pos = find_start_pos(world)[0]
    total_keys = find_num_keys(world)

    start_state = State(start_pos, frozenset(), 0)
    visited = {(start_state.pos, start_state.keys)}
    queue = deque([start_state])
    while queue:
        state = queue.popleft()
        if len(state.keys) == total_keys:
            return state.num_steps

        for neighbour in neighbours(state.pos):
            keys = state.keys
            if w(neighbour) == "#":
                continue
            elif w(neighbour) in KEYS:
                keys = keys | {w(neighbour)}
            elif w(neighbour) in DOORS:
                if w(neighbour).lower() not in state.keys:
                    continue
            k = (neighbour, keys)
            if k not in visited:
                visited.add(k)
                queue.append(State(neighbour, keys, state.num_steps + 1))


def find_all_keys(world):
    keys = {}
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col].islower():
                keys[world[row][col]] = row, col
    return keys


def reachable_keys_for_pos(start, world):
    def w(pos):
        return world[pos[0]][pos[1]]

    visited = {start}
    queue = deque([start])
    result = []
    while queue:
        pos = queue.popleft()
        if w(pos) in KEYS:
            result.append(w(pos))
        for neighbour in neighbours(pos):
            if w(neighbour) != "#" and neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return frozenset(result)


def solve_quadrant(world, start_pos, keys_in_quadrant):
    def w(pos):
        return world[pos[0]][pos[1]]

    start_state = State(start_pos, frozenset(), 0)
    visited = {(start_state.pos, start_state.keys)}
    queue = deque([start_state])
    while queue:
        state = queue.popleft()
        if len(state.keys) == len(keys_in_quadrant):
            return state.num_steps

        for neighbour in neighbours(state.pos):
            keys = state.keys
            if w(neighbour) == "#":
                continue
            elif w(neighbour) in KEYS:
                keys = keys | {w(neighbour)}
            elif w(neighbour) in DOORS:
                required_key = w(neighbour).lower()
                if required_key in keys_in_quadrant and required_key not in state.keys:
                    continue
            k = (neighbour, keys)
            if k not in visited:
                visited.add(k)
                queue.append(State(neighbour, keys, state.num_steps + 1))


def b(world):
    starts = find_start_pos(world)
    keys_per_start = [reachable_keys_for_pos(start, world) for start in starts]
    return sum(
        solve_quadrant(world, start, keys)
        for start, keys in zip(starts, keys_per_start)
    )


def main():
    world = open("input18.txt").read().splitlines()
    print(b(world))


if __name__ == "__main__":
    main()
