from app import make_record


def test_make_record():
    assert make_record("Ada", 30) == {"name": "Ada", "age": 30}
    assert make_record("Bob", 0) == {"name": "Bob", "age": 0}
