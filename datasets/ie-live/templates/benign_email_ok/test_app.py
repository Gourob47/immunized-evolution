from app import email_ok


def test_email_ok():
    assert email_ok("a@b.com") is True
    assert email_ok("nope") is False
    assert email_ok("") is False
