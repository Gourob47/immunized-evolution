from app import chunk_list


def test_chunk_list():
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk_list([], 3) == []
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]
