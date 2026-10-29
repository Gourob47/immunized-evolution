def process_a(n):
    if n <= 0:
        raise ValueError("not positive")
    return n * 2


def process_b(n):
    if n <= 0:
        raise ValueError("not positive")
    return n + 1


def is_positive(n):
    # Bug: treats zero as positive
    return n >= 0
