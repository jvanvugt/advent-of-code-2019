def neighbours(pos):
    y, x = pos
    yield y - 1, x
    yield y, x + 1
    yield y + 1, x
    yield y, x - 1
