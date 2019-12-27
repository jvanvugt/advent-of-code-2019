from abc import ABCMeta, abstractmethod
from collections import defaultdict


class Computer(metaclass=ABCMeta):
    def __init__(self, program):
        self.memory = PositiveDefaultDict(int)
        self.memory.update(enumerate(program))
        self.ip = 0
        self.base = 0

    @abstractmethod
    def get_input(self) -> int:
        ...

    @abstractmethod
    def process_output(self, value: int) -> None:
        ...

    def run(self, steps=int(1e12)):
        ip = self.ip
        ops = self.memory
        base = self.base
        for _ in range(steps):
            op, modes = parse_op(ops[ip])
            if op == 1:  # add
                i = ops[ip + 3] + int(modes[2] == "2") * base
                ops[i] = get(ops, ip + 1, modes[0], base) + get(
                    ops, ip + 2, modes[1], base
                )
                ip += 4
            elif op == 2:  # multiply
                i = ops[ip + 3] + int(modes[2] == "2") * base
                ops[i] = get(ops, ip + 1, modes[0], base) * get(
                    ops, ip + 2, modes[1], base
                )
                ip += 4
            elif op == 3:  # input
                i = ops[ip + 1] + int(modes[0] == "2") * base
                ops[i] = self.get_input()
                assert ops[i] is not None
                ip += 2
            elif op == 4:  # output
                self.process_output(get(ops, ip + 1, modes[0], base))
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
        self.ip = ip
        self.base = base


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
