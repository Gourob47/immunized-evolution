from app import abs_delta


def test_abs_delta():
    assert abs_delta(10, 3) == 7
    assert abs_delta(3, 10) == 7
    assert abs_delta(4, 4) == 0
