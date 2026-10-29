from app import VERSION, get_version


def test_version():
    assert VERSION == "2.0.0"
    assert get_version() == "2.0.0"
