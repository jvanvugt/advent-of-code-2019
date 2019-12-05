def parse_op(op):
    sop = str(op)[::-1]
    instr, modes = int(sop[:2][::-1]), sop[2:]
    return instr, modes + "0" * 4


def get(ops, ip, mode):
    if mode == "0":
        return ops[ops[ip]]
    elif mode == "1":
        return ops[ip]
    raise ValueError(mode)


def a(ops):
    ip = 0
    while ip < len(ops):
        op, modes = parse_op(ops[ip])
        if op == 1:  # add
            ops[ops[ip + 3]] = get(ops, ip + 1, modes[0]) + get(ops, ip + 2, modes[1])
            ip += 4
        elif op == 2:  # multiply
            ops[ops[ip + 3]] = get(ops, ip + 1, modes[0]) * get(ops, ip + 2, modes[1])
            ip += 4
        elif op == 3:  # input
            ops[ops[ip + 1]] = int(input())
            ip += 2
        elif op == 4:  # output
            print(get(ops, ip + 1, modes[0]))
            ip += 2
        elif op == 5:  # jump-if-true
            if get(ops, ip + 1, modes[0]) != 0:
                ip = get(ops, ip + 2, modes[1])
            else:
                ip += 3
        elif op == 6:  # jump-if-false
            if get(ops, ip + 1, modes[0]) == 0:
                ip = get(ops, ip + 2, modes[1])
            else:
                ip += 3
        elif op == 7:  # less than
            ops[ops[ip + 3]] = int(
                get(ops, ip + 1, modes[0]) < get(ops, ip + 2, modes[1])
            )
            ip += 4
        elif op == 8:  # equals
            ops[ops[ip + 3]] = int(
                get(ops, ip + 1, modes[0]) == get(ops, ip + 2, modes[1])
            )
            ip += 4
        elif op == 99:
            break
        else:
            raise ValueError(op)


def main():
    opcodes = list(map(int, open("input05.txt").read().split(",")))
    a(opcodes)


if __name__ == "__main__":
    main()
