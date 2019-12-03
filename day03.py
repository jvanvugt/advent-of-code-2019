from collections import defaultdict


def fill_wire(wire, grid, pos, name):
    crossings = []
    for instr in wire:
        direction, length = instr[0], int(instr[1:])
        for _ in range(length):
            if direction == "D":
                pos[1] += 1
            elif direction == "U":
                pos[1] -= 1
            elif direction == "L":
                pos[0] -= 1
            elif direction == "R":
                pos[0] += 1

            if grid[tuple(pos)] not in [name, "."]:
                crossings.append(tuple(pos))
            else:
                grid[tuple(pos)] = name
    return crossings


def fill_wire_steps(wire, grid, pos, name):
    steps = 0
    crossings = []
    for instr in wire:
        direction, length = instr[0], int(instr[1:])
        for _ in range(length):
            if direction == "D":
                pos[1] += 1
            elif direction == "U":
                pos[1] -= 1
            elif direction == "L":
                pos[0] -= 1
            elif direction == "R":
                pos[0] += 1
            steps += 1

            tpos = tuple(pos)
            if grid[tpos] == ".":
                grid[tpos] = f"{name}:{steps}"
            elif not grid[tpos].startswith(name):
                crossings.append(steps + int(grid[tpos].split(":")[1]))

    return crossings


def a(wire1, wire2):
    grid = defaultdict(lambda: ".")
    fill_wire(wire1, grid, [0, 0], "1")
    crossings = fill_wire(wire2, grid, [0, 0], "2")
    closest = min(abs(x) + abs(y) for x, y in crossings)
    return closest


def b(wire1, wire2):
    grid = defaultdict(lambda: ".")
    fill_wire_steps(wire1, grid, [0, 0], "1")
    crossings = fill_wire_steps(wire2, grid, [0, 0], "2")
    closest = min(crossings)
    return closest


def main():
    wire1, wire2 = map(lambda s: s.split(","), open("input03.txt").read().splitlines())
    print(b(wire1, wire2))


if __name__ == "__main__":
    main()
