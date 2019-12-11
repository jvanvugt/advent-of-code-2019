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


def run_intcode(program):
    ops = PositiveDefaultDict(int)
    for i, v in enumerate(program):
        ops[i] = v
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
            ops[i] = yield
            assert ops[i] is not None
            ip += 2
        elif op == 4:  # output
            yield get(ops, ip + 1, modes[0], base)
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


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def paint(program, *, start):
    computer = run_intcode(program)
    computer.send(None)
    pos = (0, 0)
    d = 0
    grid = defaultdict(int)
    grid[pos] = start
    while True:
        try:
            x = computer.send(grid[pos])
            grid[pos] = x
            move = next(computer)
            next(computer)
            d = (d + 1 if move == 1 else d - 1) % 4
            pos = pos[0] + DIRECTIONS[d][0], pos[1] + DIRECTIONS[d][1]
        except StopIteration:
            break
    return grid


def a(program):
    grid = paint(program, start=0)
    return len(grid.keys())


def draw_grid(grid):
    min_x = min(x for x, _ in grid.keys())
    max_x = max(x for x, _ in grid.keys())
    min_y = min(y for _, y in grid.keys())
    max_y = max(y for _, y in grid.keys())
    g = [["." for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    for (x, y), v in grid.items():
        g[y - min_y][x - min_x] = "." if v == 0 else "#"
    return "\n".join("".join(row) for row in g)


def b(program):
    grid = paint(program, start=1)
    return draw_grid(grid)


def main():
    opcodes = list(map(int, open("input11.txt").read().split(",")))
    print(b(opcodes))


if __name__ == "__main__":
    main()
