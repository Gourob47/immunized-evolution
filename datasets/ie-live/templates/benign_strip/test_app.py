from app import strip_spaces


def test_strip_spaces():
    assert strip_spaces("  hi  ") == "hi"
    assert strip_spaces("nope") == "nope"
    assert strip_spaces("   ") == ""
