def a(ops):
    for i in range(0, len(ops), 4):
        op = ops[i]
        if op == 1:
            ops[ops[i + 3]] = ops[ops[i + 1]] + ops[ops[i + 2]]
        elif op == 2:
            ops[ops[i + 3]] = ops[ops[i + 1]] * ops[ops[i + 2]]
        elif op == 99:
            break
        else:
            raise ValueError(op)
    return ops[0]


def b(ops):
    for noun in range(1, 100):
        for verb in range(1, 100):
            ops_copy = ops[:]
            ops_copy[1] = noun
            ops_copy[2] = verb
            try:
                res = a(ops_copy)
            except:
                pass
            if res == 19690720:
                return 100 * noun + verb


def main():
    opcodes = list(map(int, open("input02.txt").read().split(",")))
    opcodes[1] = 12
    opcodes[2] = 2
    print(b(opcodes))


if __name__ == "__main__":
    main()
