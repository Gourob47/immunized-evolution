def get_field(record, key, default):
    # Bug: KeyError on missing instead of default
    return record[key]
