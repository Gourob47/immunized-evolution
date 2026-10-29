from app import is_palindrome


def test_is_palindrome():
    assert is_palindrome("Racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("a") is True
