from app import filter_positive


def test_filter_positive():
    assert filter_positive([1, -2, 3, 0, -5]) == [1, 3]
    assert filter_positive([]) == []
    assert filter_positive([-1, -2]) == []
