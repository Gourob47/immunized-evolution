def slugify(text):
    # Bug: only lowercases; does not hyphenate or strip punctuation
    return text.lower()
