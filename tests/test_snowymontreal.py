import snowymontreal
from tests.tools import is_solved


def test_solve():
    edges = [
        (0, 1, 1), (1, 2, 1), (2, 3, 1), (2, 24, 6), (1, 3, 1), (1, 23, 7), (3, 4, 3), (4, 5, 1), (4, 25, 6),
        (5, 6, 1), (5, 7, 1), (7, 8, 12), (7, 25, 7), (8, 9, 5), (8, 18, 4), (9, 10, 1), (9, 18, 1), (9, 11, 2),
        (11, 12, 4), (11, 17, 1), (12, 13, 1), (12, 14, 1), (12, 15, 4), (16, 17, 8), (17, 18, 1), (17, 19, 1),
        (18, 19, 1), (19, 20, 5), (20, 21, 1), (21, 22, 1), (21, 23, 5), (20, 24, 4), (23, 24, 3), (24, 25, 1),
        (25, 26, 1)
    ]

    # Not directed
    cycle = snowymontreal.solve(False, 27, edges)
    assert is_solved(edges, cycle)

    # Directed
    cycle = snowymontreal.solve(True, 27, edges)
    assert is_solved(edges, cycle)
