from app import count_zeros


def test_count_zeros():
    assert count_zeros([0, 1, 0, None, 2]) == 2
    assert count_zeros([]) == 0
    assert count_zeros([None, None]) == 0
