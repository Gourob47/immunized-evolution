import pytest
from app import fail_fast


def test_fail_fast():
    with pytest.raises(ValueError) as exc:
        fail_fast()
    assert str(exc.value) == "invalid input received"
