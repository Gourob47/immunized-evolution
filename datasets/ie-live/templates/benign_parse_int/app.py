def parse_int(s):
    # Bug: empty string becomes 0 instead of ValueError
    if s == '':
        return 0
    return int(s)
