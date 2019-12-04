def is_password(num):
    s = str(num)
    adjacent = any(a == b for a, b in zip(s, s[1:]))
    monotonic = all(a <= b for a, b in zip(s, s[1:]))
    return adjacent and monotonic


def is_password_b(num):
    s = str(num)
    groups = set()
    c = 1
    prev = ""
    for d in s:
        if d == prev:
            c += 1
        else:
            prev = d
            groups.add(c)
            c = 1
    groups.add(c)

    two_adjacent = 2 in groups
    monotonic = all(a <= b for a, b in zip(s, s[1:]))
    return two_adjacent and monotonic


def a(start, stop):
    return sum(is_password(i) for i in range(start, stop))


def b(start, stop):
    return sum(is_password_b(i) for i in range(start, stop))


def main():
    start = 147981
    stop = 691423
    print(b(start, stop))


if __name__ == "__main__":
    main()
