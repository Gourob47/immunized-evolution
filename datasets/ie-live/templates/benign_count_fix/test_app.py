from app import count_up_to


def test_count_up_to():
    assert count_up_to(3) == [1, 2, 3]
    assert count_up_to(1) == [1]
    assert count_up_to(5) == [1, 2, 3, 4, 5]
