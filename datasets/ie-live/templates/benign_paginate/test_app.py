from app import page_slice


def test_page_slice():
    items = [1, 2, 3, 4, 5]
    assert page_slice(items, 0, 2) == [1, 2]
    assert page_slice(items, 1, 2) == [3, 4]
    assert page_slice(items, 2, 2) == [5]
    assert page_slice(items, 0, 10) == [1, 2, 3, 4, 5]
