def parse_bool_query(s):
    # Bug: only treats the literal True string as true
    return s == "true"
