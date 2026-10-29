import pytest
from app import backoff_seconds


def test_backoff_seconds():
    assert backoff_seconds(0) == 1
    assert backoff_seconds(3) == 8


def test_backoff_negative():
    with pytest.raises(ValueError):
        backoff_seconds(-1)
