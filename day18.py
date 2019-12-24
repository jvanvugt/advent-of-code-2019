import string

from dataclasses import dataclass
from typing import Tuple, FrozenSet, NamedTuple
from collections import deque
from utils import neighbours


KEYS = set(string.ascii_lowercase)
DOORS = set(string.ascii_uppercase)


def find_start_pos(world):
    starts = []
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col] == "@":
                starts.append((row, col))
    return starts


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


Pos = Tuple[int, int]


@dataclass
class State4(NamedTuple):
    pos: Tuple[Pos, Pos, Pos, Pos]
    keys: FrozenSet[set]
    num_steps: int


def b(world):
    def w(pos):
        return world[pos[0]][pos[1]]

    starts = tuple(find_start_pos(world))
    total_keys = find_num_keys(world)

    start_state = State4(starts, frozenset(), 0)
    visited = {(start_state.pos, start_state.keys)}
    queue = deque([start_state])
    i = -1
    while queue:
        state = queue.popleft()
        if state.num_steps > i:
            i = state.num_steps
            print(i, len(queue))
        if len(state.keys) == total_keys:
            return state.num_steps

        for robot in range(4):
            for neighbour in neighbours(state.pos[robot]):
                keys = state.keys
                if w(neighbour) == "#":
                    continue
                elif w(neighbour) in KEYS:
                    keys = keys | {w(neighbour)}
                elif w(neighbour) in DOORS:
                    if w(neighbour).lower() not in state.keys:
                        continue
                new_pos = state.pos[:robot] + (neighbour,) + state.pos[robot + 1 :]
                k = (new_pos, keys)
                if k not in visited:
                    visited.add(k)
                    queue.append(State4(new_pos, keys, state.num_steps + 1))


def main():
    world = open("input18.txt").read().splitlines()
    print(b(world))


if __name__ == "__main__":
    main()
