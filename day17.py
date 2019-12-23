from intcode import Computer
from io import StringIO
from collections import defaultdict


class AComputer(Computer):
    def __init__(self, program, out):
        self.out = out
        super().__init__(program)

    def process_output(self, o):
        self.out.write(chr(o))

    def get_input(self):
        raise NotImplementedError()


def neighbours(pos):
    y, x = pos
    yield y - 1, x
    yield y, x + 1
    yield y + 1, x
    yield y, x - 1


def a(program):
    out_buffer = StringIO()
    computer = AComputer(program, out_buffer)
    computer.run()
    s = out_buffer.getvalue()
    grid = [list(line) for line in s.splitlines()]
    d = {}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            d[row, col] = grid[row][col]

    intersections = []
    for pos, v in d.items():
        if v == "#":
            if all(d.get(n, ".") == "#" for n in neighbours(pos)):
                intersections.append(pos)
    return sum(x * y for x, y in intersections)


def to_ascii(s):
    return list(map(ord, s))


class BComputer(Computer):
    def __init__(self, program):
        inputs = [
            *to_ascii("A,B,A,B,A,C,B,C,A,C\n"),  # main
            *to_ascii("R,4,L,10,L,10\n"),  # A
            *to_ascii("L,8,R,12,R,10,R,4\n"),  # B
            *to_ascii("L,8,L,8,R,10,R,4\n"),  # C
            *to_ascii("n\n"),
        ]
        self.inputs = iter(inputs)
        self.last_output = 0

        super().__init__(program)

    def process_output(self, o):
        print(chr(o), end="")
        self.last_output = o

    def get_input(self):
        return next(self.inputs)


def b(program):
    program[0] = 2
    computer = BComputer(program)
    computer.run()
    return computer.last_output


def main():
    program = list(map(int, open("input17.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
