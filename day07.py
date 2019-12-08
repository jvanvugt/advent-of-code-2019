import itertools


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


def run_intcode(ops):
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
            ops[ops[ip + 1]] = yield
            ip += 2
        elif op == 4:  # output
            yield get(ops, ip + 1, modes[0])
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


def run_amps(program, phase_setting):
    input_value = 0
    for phase in phase_setting:
        amp = run_intcode(program[:])
        amp.send(None)
        amp.send(phase)
        input_value = amp.send(input_value)
    return input_value


def a(program):
    return max(
        run_amps(program, phase_settings)
        for phase_settings in itertools.permutations(range(5))
    )


def run_amps_feedback(program, phase_setting):
    amps = [run_intcode(program[:]) for _ in range(len(phase_setting))]
    for amp, phase in zip(amps, phase_setting):
        amp.send(None)
        amp.send(phase)

    value = 0
    halted = 0
    for amp in itertools.cycle(amps):
        try:
            value = amp.send(value)
            next(amp)
        except StopIteration:
            halted += 1
            if halted == 5:
                return value


def b(program):
    return max(
        run_amps_feedback(program, phase_settings)
        for phase_settings in itertools.permutations(range(5, 10))
    )


def main():
    program = list(map(int, open("input07.txt").read().split(",")))
    print(a(program))


if __name__ == "__main__":
    main()
