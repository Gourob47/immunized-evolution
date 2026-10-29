from app import get_field


def test_get_field():
    r = {"name": "Ada"}
    assert get_field(r, "name", None) == "Ada"
    assert get_field(r, "age", 0) == 0
    assert get_field({}, "x", "missing") == "missing"
