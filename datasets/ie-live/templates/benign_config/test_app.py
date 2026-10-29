from app import DEFAULT_TIMEOUT, get_timeout


def test_timeout():
    assert DEFAULT_TIMEOUT == 60
    assert get_timeout() == 60
