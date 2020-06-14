import drone


def test_solve():
    edges = []
    assert drone.solve(0, edges) == []

    edges = [
        (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7), (2, 8, 2), (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10),
        (5, 6, 2), (6, 7, 1), (6, 8, 6), (7, 8, 7)
    ]
    assert drone.solve(9, edges) == [2, 5, 6, 8, 2]
