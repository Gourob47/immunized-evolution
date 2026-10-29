from app import sort_asc


def test_sort_asc():
    assert sort_asc([3, 1, 2]) == [1, 2, 3]
    assert sort_asc([]) == []
    assert sort_asc([5]) == [5]
