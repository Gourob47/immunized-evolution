from app import is_positive, process_a, process_b


def test_is_positive():
    assert is_positive(5) is True
    assert is_positive(0) is False
    assert is_positive(-1) is False


def test_process():
    assert process_a(3) == 6
    assert process_b(3) == 4
