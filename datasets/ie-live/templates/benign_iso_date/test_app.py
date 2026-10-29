from app import format_iso_date


def test_format_iso_date():
    assert format_iso_date(2026, 10, 13) == "2026-10-13"
    assert format_iso_date(2026, 1, 5) == "2026-01-05"
    assert format_iso_date(1999, 12, 1) == "1999-12-01"
