from app import get_name


def test_get_name():
    assert get_name('{"name": "Ada", "age": 30}') == "Ada"
    assert get_name('{"name": "Bob"}') == "Bob"
