from copy import deepcopy
from utils import neighbours


N = 5


def s(world):
    return "\n".join("".join(row) for row in world)


def count_bugs(world, row, col):
    bugs = 0
    for neighbour in neighbours((row, col)):
        row, col = neighbour
        if 0 <= row < N and 0 <= col < N:
            if world[row][col] == "#":
                bugs += 1
    return bugs


def find_repeating(world):
    seen = {s(world)}
    while True:
        new_world = deepcopy(world)
        for row in range(5):
            for col in range(5):
                if world[row][col] == "#" and count_bugs(world, row, col) != 1:
                    new_world[row][col] = "."
                elif world[row][col] == "." and count_bugs(world, row, col) in [1, 2]:
                    new_world[row][col] = "#"
        world = new_world
        k = s(world)
        if k in seen:
            return world
        seen.add(k)


def a(world):
    repeating = find_repeating(world)
    diversity = 0
    for row in range(N):
        for col in range(N):
            if repeating[row][col] == "#":
                i = row * N + col
                diversity += 2 ** i
    return diversity


def recursive_neighbours(level, row, col):
    if row != 2 or col != 2:
        for neighbour in neighbours((row, col)):
            if 0 <= neighbour[0] < N and 0 <= neighbour[1] < N and neighbour != (2, 2):
                yield (level, *neighbour)
    if row == 0:
        yield (level - 1, 1, 2)
    elif row == 4:
        yield (level - 1, 3, 2)
    if col == 0:
        yield (level - 1, 2, 1)
    elif col == 4:
        yield (level - 1, 2, 3)

    if row == 1 and col == 2:
        for x in range(N):
            yield (level + 1, 0, x)
    elif row == 3 and col == 2:
        for x in range(N):
            yield (level + 1, 4, x)
    elif col == 1 and row == 2:
        for x in range(N):
            yield (level + 1, x, 0)
    elif col == 3 and row == 2:
        for x in range(N):
            yield (level + 1, x, 4)


def b(world):
    steps = 200

    bugs = set()
    for row in range(N):
        for col in range(N):
            if world[row][col] == "#":
                bugs.add((0, row, col))

    for _ in range(steps):
        new_bugs = set()
        dead_bugs = set()
        for bug in bugs:
            num_neighbours = sum(
                neighbour in bugs for neighbour in recursive_neighbours(*bug)
            )
            if num_neighbours != 1:
                dead_bugs.add(bug)
        for bug in bugs:
            for neighbour in recursive_neighbours(*bug):
                if neighbour not in bugs:
                    num_neighbours = sum(
                        neigh in bugs for neigh in recursive_neighbours(*neighbour)
                    )
                    if num_neighbours in [1, 2]:
                        new_bugs.add(neighbour)

        bugs = (bugs - dead_bugs) | new_bugs

    return len(bugs)


def main():
    world = [list(line) for line in open("input24.txt").read().splitlines()]
    print(b(world))


if __name__ == "__main__":
    main()
