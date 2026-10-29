import pytest
from app import unit_price


def test_unit_price():
    assert unit_price(10, 2) == 5.0
    assert unit_price(7, 2) == 3.5


def test_unit_price_zero():
    with pytest.raises(ZeroDivisionError):
        unit_price(1, 0)
