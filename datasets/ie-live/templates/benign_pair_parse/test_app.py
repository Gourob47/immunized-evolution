from app import parse_pair


def test_parse_pair():
    assert parse_pair("3 7") == (3, 7)
    assert parse_pair("0 -1") == (0, -1)
