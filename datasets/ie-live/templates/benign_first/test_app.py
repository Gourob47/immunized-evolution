from app import first_or_none


def test_first_or_none():
    assert first_or_none([10, 20]) == 10
    assert first_or_none([]) is None
    assert first_or_none(["a"]) == "a"
