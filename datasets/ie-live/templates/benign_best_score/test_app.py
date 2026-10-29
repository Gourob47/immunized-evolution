from app import best_score


def test_best_score():
    assert best_score(3, 7) == 7
    assert best_score(10, 2) == 10
    assert best_score(-1, -5) == -1
