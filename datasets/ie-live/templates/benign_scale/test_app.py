from app import scale_scores


def test_scale_scores():
    assert scale_scores([1, 2, 3], 2) == [2, 4, 6]
    assert scale_scores([], 3) == []
    assert scale_scores([-1], 2) == [-2]
