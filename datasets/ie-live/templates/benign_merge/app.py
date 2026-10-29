def merge_dicts(a, b):
    # Bug: prefers a on conflict and mutates a
    a.update(b)
    return b
