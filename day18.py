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


Pos = Tuple[int, int]


@dataclass
class State4(NamedTuple):
    pos: Tuple[Pos, Pos, Pos, Pos]
    keys: FrozenSet[set]
    num_steps: int


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


def find_shortest_path(world, goal_pos, pos):
    def w(pos):
        return world[pos[0]][pos[1]]

    visited = {(pos, frozenset())}
    queue = deque([(pos, frozenset(), 0, "")])
    while queue:
        pos, keys_required, steps, keys_along = queue.popleft()
        if pos == goal_pos:
            return (steps, keys_required, keys_along)
        for neighbour in neighbours(pos):
            nk = keys_required
            new_keys_along = keys_along
            if w(neighbour) == "#":
                continue
            if w(neighbour).isupper():
                nk = nk | {w(neighbour).lower()}
            if w(neighbour).islower():
                new_keys_along = keys_along + w(neighbour)
            k = (neighbour, nk)
            if k not in visited:
                visited.add(k)
                queue.append((neighbour, nk, steps + 1, new_keys_along))
    raise ValueError()


def find_all_keys(world):
    keys = {}
    for row in range(len(world)):
        for col in range(len(world[row])):
            if world[row][col].islower():
                keys[world[row][col]] = row, col
    return keys


def b(world):
    starts = find_start_pos(world)
    all_keys = find_all_keys(world)
    keys_per_start = [reachable_keys_for_pos(start, world) for start in starts]
    shortest_paths = {}
    for start, keys in zip(starts, keys_per_start):
        pois = [start] + [all_keys[k] for k in keys]
        for i in range(len(pois)):
            for j in range(i + 1, len(pois)):
                pos1 = pois[i]
                pos2 = pois[j]
                steps, keys_required, keys_along = find_shortest_path(world, pos2, pos1)
                shortest_paths[pos1, pos2] = steps, keys_required
                shortest_paths[pos2, pos1] = shortest_paths[pos1, pos2]

    queue = [(0, starts, "")]
    visited = {""}
    i = 0
    while queue:
        num_steps, positions, collected_keys = heapq.heappop(queue)
        if num_steps > i:
            i = num_steps
            print(i)
        if len(collected_keys) == len(all_keys):
            return num_steps

        for robot in range(len(starts)):
            for key in keys_per_start[robot]:
                if key in collected_keys:
                    continue

                key_pos = all_keys[key]
                steps, keys_required = shortest_paths[positions[robot], key_pos]
                if all(k in collected_keys for k in keys_required):
                    new_pos = positions[:robot] + (key_pos,) + positions[robot + 1 :]
                    new_keys = collected_keys + key
                    k = new_keys
                    if k not in visited:
                        visited.add(k)
                        heapq.heappush(queue, (num_steps + steps, new_pos, new_keys))


def main():
    world = open("input18.txt").read().splitlines()
    print(b(world))


if __name__ == "__main__":
    main()
