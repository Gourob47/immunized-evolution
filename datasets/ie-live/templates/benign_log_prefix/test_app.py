from app import log_prefix


def test_log_prefix():
    assert log_prefix("started") == "[INFO] started"
    assert log_prefix("") == "[INFO] "
