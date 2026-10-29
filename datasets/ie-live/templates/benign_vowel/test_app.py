from app import starts_with_vowel


def test_starts_with_vowel():
    assert starts_with_vowel("apple") is True
    assert starts_with_vowel("Banana") is False
    assert starts_with_vowel("Orange") is True
    assert starts_with_vowel("") is False
