from app import flatten_one_level


def test_flatten_one_level():
    assert flatten_one_level([[1, 2], [3]]) == [1, 2, 3]
    assert flatten_one_level([]) == []
    assert flatten_one_level([[], [4]]) == [4]
