def chunk_list(items, size):
    # Bug: returns the original list wrapped once
    return [list(items)]
