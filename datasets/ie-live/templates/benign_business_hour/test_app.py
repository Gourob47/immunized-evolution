from app import is_business_hour


def test_is_business_hour():
    assert is_business_hour(9) is True
    assert is_business_hour(17) is True
    assert is_business_hour(8) is False
    assert is_business_hour(18) is False
