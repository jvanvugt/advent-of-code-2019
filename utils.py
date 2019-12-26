def neighbours(pos, diagonal=False):
    y, x = pos
    yield y - 1, x
    yield y, x + 1
    yield y + 1, x
    yield y, x - 1
    if diagonal:
        yield y - 1, x - 1
        yield y - 1, x + 1
        yield y + 1, x + 1
        yield y + 1, x - 1
