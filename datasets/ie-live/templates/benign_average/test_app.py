from app import average


def test_average():
    assert average([2, 4, 6]) == 4.0
    assert average([10]) == 10.0
    assert average([]) is None
