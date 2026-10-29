from app import unique_items


def test_unique_items():
    assert unique_items([1, 2, 1, 3, 2]) == [1, 2, 3]
    assert unique_items([]) == []
    assert unique_items(["a", "a"]) == ["a"]
