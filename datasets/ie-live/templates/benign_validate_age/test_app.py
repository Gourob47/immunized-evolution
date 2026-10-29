import pytest
from app import validate_age


def test_validate_age_ok():
    assert validate_age(0) is True
    assert validate_age(25) is True
    assert validate_age(120) is True


def test_validate_age_bad():
    with pytest.raises(ValueError):
        validate_age(-1)
    with pytest.raises(ValueError):
        validate_age(121)
    with pytest.raises(ValueError):
        validate_age(3.5)
