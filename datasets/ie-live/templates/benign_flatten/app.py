def flatten_one_level(nested):
    # Bug: empty outer list returns None instead of []
    if not nested:
        return None
    result = []
    for item in nested:
        result.extend(item)
    return result
