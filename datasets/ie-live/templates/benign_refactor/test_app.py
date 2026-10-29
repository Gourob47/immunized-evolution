from app import sum_list


def test_sum_list():
    assert sum_list([1, 2, 3]) == 6
    assert sum_list([10]) == 10
    assert sum_list([]) == 0
