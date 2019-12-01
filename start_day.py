#! /usr/bin/env python
from pathlib import Path
import sys


TEMPLATE = """
def a():
    ...


def b():
    ...


def main():
    open("input{day}.txt")
    print(a(...))


if __name__ == "__main__":
    main()
""".lstrip("\n")


def main():
    day = f"{int(sys.argv[1]):02d}"
    code = TEMPLATE.format(day=day)
    code_file = Path(f"day{day}.py")
    input_file = Path(f"input{day}.txt")
    if code_file.exists() or input_file.exists():
        raise ValueError(f"Day {day} already exists!")

    code_file.open("w").write(code)
    input_file.open("w").write("")


if __name__ == "__main__":
    main()
