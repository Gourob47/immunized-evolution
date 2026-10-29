from app import cheapest


def test_cheapest():
    assert cheapest(3, 7) == 3
    assert cheapest(10, 2) == 2
    assert cheapest(-1, -5) == -5
