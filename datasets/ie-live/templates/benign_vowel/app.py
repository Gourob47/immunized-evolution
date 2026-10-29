def starts_with_vowel(s):
    # Bug: case-sensitive and treats y as a vowel
    return bool(s) and s[0] in 'aeiouy'
