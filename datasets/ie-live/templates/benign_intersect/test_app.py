from app import intersection


def test_intersection():
    assert intersection([1, 2, 3], [2, 3, 4]) == [2, 3]
    assert intersection([], [1]) == []
    assert intersection([5], [5]) == [5]
