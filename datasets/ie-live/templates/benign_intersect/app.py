def intersection(a, b):
    # Bug: unsorted union
    return list(set(a) | set(b))
