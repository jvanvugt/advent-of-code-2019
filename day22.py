def a(instructions):
    N = 10007
    cards = list(range(N))
    temp_cards = cards.copy()
    for instr in instructions:
        if "increment" in instr:
            incr = int(instr.split(" ")[-1])
            for c in range(N):
                temp_cards[(incr * c) % N] = cards[c]
            cards, temp_cards = temp_cards, cards
        elif "stack" in instr:
            cards = cards[::-1]
        elif "cut" in instr:
            amount = int(instr.split(" ")[-1])
            cards = cards[amount:] + cards[:amount]
    return cards.index(2019)


def inv(n, mod):
    return pow(n, mod - 2, mod)


def b(instructions):
    # Credits: https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
    N = 119315717514047
    times = 101741582076661
    position = 2020
    offset = 0
    incr = 1
    for instr in instructions:
        if "increment" in instr:
            amount = int(instr.split(" ")[-1])
            incr *= inv(amount, N)
        elif "stack" in instr:
            incr *= -1
            offset += incr
        elif "cut" in instr:
            amount = int(instr.split(" ")[-1])
            offset += incr * amount
    old_incr = incr
    incr = pow(incr, times, N)
    offset = offset * (1 - incr) * inv(1 - old_incr, N)
    card = (offset + incr * position) % N
    return card


def main():
    instructions = open("input22.txt").read().splitlines()
    print(b(instructions))


if __name__ == "__main__":
    main()
