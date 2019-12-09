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
        super().__missing__(i)


def a(program):
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
            ops[i] = int(input())
            ip += 2
        elif op == 4:  # output
            print(get(ops, ip + 1, modes[0], base))
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


def main():
    opcodes = list(map(int, open("input09.txt").read().split(",")))
    a(opcodes)


if __name__ == "__main__":
    main()
