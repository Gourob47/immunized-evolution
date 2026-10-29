from app import merge_dicts


def test_merge_dicts():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_dicts({"x": 1}, {"x": 9}) == {"x": 9}
    assert merge_dicts({}, {"k": 0}) == {"k": 0}
