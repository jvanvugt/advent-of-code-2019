from intcode import Computer
import itertools


def to_ascii(s):
    return list(map(ord, s))


class AsciiComputer(Computer):
    def __init__(self, program, inputs):
        self.inputs = iter(inputs)

        super().__init__(program)

    def process_output(self, o):
        if o > 256:
            print(o)
        else:
            print(chr(o), end="")

    def get_input(self):
        return next(self.inputs)


def a(program):
    # (~A or ~B or ~C) and D
    springprogram = [
        *to_ascii("NOT A J\n"),
        *to_ascii("NOT B T\n"),
        *to_ascii("OR T J\n"),
        *to_ascii("NOT C T\n"),
        *to_ascii("OR T J\n"),
        *to_ascii("AND D J\n"),
        *to_ascii("WALK\n"),
    ]
    computer = AsciiComputer(program, springprogram)
    computer.run()


def b(program):
    springprogram = [
        # (~A or ~B or ~C) and D and (H or E)
        *to_ascii("NOT A J\n"),
        *to_ascii("NOT B T\n"),
        *to_ascii("OR T J\n"),
        *to_ascii("NOT C T\n"),
        *to_ascii("OR T J\n"),
        *to_ascii("AND D J\n"),
        *to_ascii("NOT D T\n"),  # reset T
        *to_ascii("OR H T\n"),
        *to_ascii("OR E T\n"),
        *to_ascii("AND T J\n"),
        *to_ascii("RUN\n"),
    ]
    computer = AsciiComputer(program, springprogram)
    computer.run()


def main():
    program = list(map(int, open("input21.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
