from app import parse_bool_query


def test_parse_bool_query():
    assert parse_bool_query("true") is True
    assert parse_bool_query("YES") is True
    assert parse_bool_query("1") is True
    assert parse_bool_query("false") is False
    assert parse_bool_query("No") is False
    assert parse_bool_query("0") is False
