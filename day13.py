from day11 import run_intcode as run_intcode_old

from collections import defaultdict


def parse_op(op):
    sop = str(op)[::-1]
    instr, modes = int(sop[:2][::-1]), sop[2:]
    return instr, modes + "0" * 4


def get(ops, ip, mode, base):
    if mode == "0":
        return ops[ops[ip]]
    elif mode == "1":
        return ops[ip]
    elif mode == "2":
        return ops[base + ops[ip]]
    raise ValueError(mode)


class PositiveDefaultDict(defaultdict):
    def __missing__(self, i):
        if i < 0:
            raise IndexError(i)
        return super().__missing__(i)


def run_intcode(program, out_fn, in_fn):
    ops = PositiveDefaultDict(int)
    ops.update(enumerate(program))
    ip = 0
    base = 0
    while ip < len(ops):
        op, modes = parse_op(ops[ip])
        if op == 1:  # add
            i = ops[ip + 3] + int(modes[2] == "2") * base
            ops[i] = get(ops, ip + 1, modes[0], base) + get(ops, ip + 2, modes[1], base)
            ip += 4
        elif op == 2:  # multiply
            i = ops[ip + 3] + int(modes[2] == "2") * base
            ops[i] = get(ops, ip + 1, modes[0], base) * get(ops, ip + 2, modes[1], base)
            ip += 4
        elif op == 3:  # input
            i = ops[ip + 1] + int(modes[0] == "2") * base
            ops[i] = in_fn()
            assert ops[i] is not None
            ip += 2
        elif op == 4:  # output
            out_fn(get(ops, ip + 1, modes[0], base))
            ip += 2
        elif op == 5:  # jump-if-true
            if get(ops, ip + 1, modes[0], base) != 0:
                ip = get(ops, ip + 2, modes[1], base)
            else:
                ip += 3
        elif op == 6:  # jump-if-false
            if get(ops, ip + 1, modes[0], base) == 0:
                ip = get(ops, ip + 2, modes[1], base)
            else:
                ip += 3
        elif op == 7:  # less than
            i = ops[ip + 3] + int(modes[2] == "2") * base
            ops[i] = int(
                get(ops, ip + 1, modes[0], base) < get(ops, ip + 2, modes[1], base)
            )
            ip += 4
        elif op == 8:  # equals
            i = ops[ip + 3] + int(modes[2] == "2") * base
            ops[i] = int(
                get(ops, ip + 1, modes[0], base) == get(ops, ip + 2, modes[1], base)
            )
            ip += 4
        elif op == 9:  # change relative-base
            base += get(ops, ip + 1, modes[0], base)
            ip += 2
        elif op == 99:
            break
        else:
            raise ValueError(op)


def draw(program):
    screen = {}

    cabinet = run_intcode_old(program)
    for x, y, tile_id in zip(cabinet, cabinet, cabinet):
        screen[x, y] = tile_id
    return screen


def a(program):
    screen = draw(program)
    return sum(tile_id == 2 for tile_id in screen.values())


def b(program):
    program[0] = 2
    width, height = 44, 24
    screen = [[" " for _ in range(width)] for _ in range(height)]
    tiles = [" ", "#", "+", "-", "O"]

    score = 0

    def get_ball_pos():
        b = None
        p = None
        for x in range(width):
            for y in range(height):
                if screen[y][x] == "O":
                    b = x, y
                elif screen[y][x] == "-":
                    p = x, y
        assert b and p
        return b, p

    def in_fn():
        print(f"Score: {score}")
        print("\n".join("".join(row) for row in screen))
        ball, player = get_ball_pos()
        if ball[0] < player[0]:
            return -1
        return int(ball[0] > player[0])

    state = {"x": 0, "y": 0, "tile_id": 0, "i": 0}

    def out_fn(a):
        nonlocal score
        i = state["i"]
        if i % 3 == 0:
            state["x"] = a
        elif i % 3 == 1:
            state["y"] = a
        elif i % 3 == 2:
            state["tile_id"] = a
            if state["x"] == -1 and state["y"] == 0:
                score = a
            else:
                x, y = state["x"], state["y"]
                screen[y][x] = tiles[state["tile_id"]]

        state["i"] += 1

    run_intcode(program, out_fn, in_fn)
    return score


def main():
    program = list(map(int, open("input13.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
