from intcode import Computer
from collections import deque
import itertools


def to_ascii(s):
    return list(map(ord, s))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


class AsciiComputer(Computer):
    def __init__(self, program):
        self.input_buffer = deque(
            [
                *to_ascii("north\nnorth\neast\neast\ntake cake\n"),
                *to_ascii("west\nwest\nsouth\nsouth\n"),
                *to_ascii("south\nwest\ntake fuel cell\nwest\ntake easter egg\n"),
                *to_ascii("east\neast\nnorth\n"),
                *to_ascii("east\ntake ornament\neast\ntake hologram\neast\n"),
                *to_ascii("take dark matter\nnorth\nnorth\neast\ntake klein bottle\n"),
                *to_ascii("north\ntake hypercube\nnorth\n"),
            ]
        )
        items = [
            "ornament",
            "easter egg",
            "hypercube",
            "hologram",
            "cake",
            "fuel cell",
            "dark matter",
            "klein bottle",
        ]
        for item in items:
            self.input_buffer.extend(to_ascii(f"drop {item}\n"))
        for combination in powerset(items):
            for item in combination:
                self.input_buffer.extend(to_ascii(f"take {item}\n"))

            self.input_buffer.extend(to_ascii("west\n"))

            for item in combination:
                self.input_buffer.extend(to_ascii(f"drop {item}\n"))

        super().__init__(program)

    def get_input(self):
        if len(self.input_buffer) > 0:
            return self.input_buffer.popleft()
        command = to_ascii(input() + "\n")
        self.input_buffer.extend(command)
        return self.input_buffer.popleft()

    def process_output(self, o):
        if o > 256:
            print(o)
        else:
            print(chr(o), end="")


def a(program):
    computer = AsciiComputer(program)
    computer.run()


def main():
    program = list(map(int, open("input25.txt").read().split(",")))
    print(a(program))


if __name__ == "__main__":
    main()
