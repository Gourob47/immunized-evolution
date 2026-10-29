from app import MAX_RETRIES, get_max_retries


def test_retries():
    assert MAX_RETRIES == 5
    assert get_max_retries() == 5
