from app import safe_len


def test_safe_len():
    assert safe_len([1, 2]) == 2
    assert safe_len("") == 0
    assert safe_len(None) == 0
