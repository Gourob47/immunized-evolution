from app import csv_sum


def test_csv_sum():
    assert csv_sum("3,5") == 8
    assert csv_sum("0,0") == 0
    assert csv_sum("-1,4") == 3
