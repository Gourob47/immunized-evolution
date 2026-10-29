import pytest
from app import parse_int


def test_parse_int():
    assert parse_int("42") == 42
    assert parse_int("0") == 0


def test_parse_int_empty():
    with pytest.raises(ValueError):
        parse_int("")
