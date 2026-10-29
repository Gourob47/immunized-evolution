from app import remaining_budget


def test_remaining_budget():
    assert remaining_budget(100, 40) == 60
    assert remaining_budget(50, 50) == 0
    assert remaining_budget(10, 0) == 10
