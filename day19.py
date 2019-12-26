from intcode import Computer
from utils import neighbours
from collections import deque
import itertools


class BeamComputer(Computer):
    def __init__(self, program, x, y):
        self.inputs = iter([x, y])
        self.res = float("nan")
        super().__init__(program)

    def process_output(self, o):
        self.res = o

    def get_input(self):
        return next(self.inputs)


def probe_location(program, x, y):
    computer = BeamComputer(program, x, y)
    computer.run()
    assert computer.res in [0, 1]
    return computer.res


def a(program):
    N = 50
    res = 0
    w = [["" for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            s = probe_location(program, x, y)
            res += s
            w[y][x] = ".#"[s]
    print("\n".join("".join(row) for row in w))
    return res


def check_square(program, right, top):
    S = 100 - 1
    return all(
        [
            probe_location(program, right - S, top),
            probe_location(program, right, top + S),
            probe_location(program, right - S, top + S),
        ]
    )


def b(program):
    pos = (6, 8)
    assert probe_location(program, *pos)
    while True:
        if check_square(program, *pos):
            return (pos[0] - 99) * 10_000 + pos[1]
        for neighbour in [(pos[0] + 1, pos[1] + 1), (pos[0], pos[1] + 1)]:
            if probe_location(program, *neighbour) == 1:
                pos = neighbour
                break
        else:
            raise ValueError()


def main():
    program = list(map(int, open("input19.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
