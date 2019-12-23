from functools import reduce


def cumsum(nums):
    return reduce(lambda l, s: l.append(s + l[-1]) or l, nums, [0])[1:]


def a(signal):
    base = [0, 1, 0, -1]
    for _ in range(100):
        out = []
        for i in range(len(signal)):
            pattern = [
                base[(j // (i + 1)) % len(base)] for j in range(1, len(signal) + 1)
            ]
            out.append(abs(sum(s * p for s, p in zip(signal, pattern))) % 10)
        signal = out
    return "".join(map(str, signal[:8]))


def b(signal):
    signal = signal * 10000
    offset = sum(10 ** i * n for i, n in enumerate(reversed(signal[:7])))
    for _ in range(100):
        updates = cumsum(signal[offset:][::-1])[::-1]
        for i in range(offset, len(signal)):
            signal[i] = updates[i - offset] % 10
    return "".join(map(str, signal[offset : offset + 8]))


def main():
    signal = list(map(int, open("input16.txt").read()))
    print(b(signal))


if __name__ == "__main__":
    main()
