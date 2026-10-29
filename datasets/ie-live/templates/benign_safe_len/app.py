def safe_len(obj):
    # Bug: crashes on None
    return len(obj)
