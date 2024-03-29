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

    edges = [
        (0, 1, 1), (1, 2, 1), (2, 3, 1), (2, 24, 6), (1, 3, 1), (1, 23, 7), (3, 4, 3), (4, 5, 1), (4, 25, 6), (5, 6, 1),
        (5, 7, 1), (7, 8, 12), (7, 25, 7), (8, 9, 5), (8, 18, 4), (9, 10, 1), (9, 18, 1), (9, 11, 2), (11, 12, 4),
        (11, 17, 1), (12, 13, 1), (12, 14, 1), (12, 15, 4), (15, 30, 1), (30, 29, 2), (29, 93, 2), (93, 16, 1),
        (16, 17, 8), (17, 18, 1), (17, 19, 1), (18, 19, 1), (19, 20, 5), (20, 21, 1), (20, 24, 4), (21, 22, 1),
        (21, 23, 5), (23, 24, 3), (24, 25, 1), (25, 26, 1), (27, 102, 3), (27, 35, 4), (27, 39, 1), (15, 31, 1),
        (31, 32, 1), (31, 30, 1), (31, 34, 3), (30, 33, 2), (33, 29, 1), (33, 35, 1), (29, 28, 3), (28, 27, 1),
        (28, 102, 5), (28, 94, 1), (16, 94, 3), (93, 94, 3), (95, 102, 2), (95, 99, 1), (95, 100, 1), (96, 99, 1),
        (97, 99, 1), (97, 98, 1), (97, 100, 1), (100, 101, 1), (94, 95, 6), (40, 102, 1), (35, 38, 1), (34, 35, 1),
        (34, 37, 1), (37, 36, 1), (37, 38, 1), (38, 39, 4), (38, 58, 2), (39, 57, 3), (39, 40, 3), (40, 41, 3),
        (40, 57, 2), (41, 42, 1), (42, 43, 2), (43, 44, 1), (43, 45, 1), (42, 45, 2), (44, 45, 1), (45, 46, 1),
        (44, 46, 1), (46, 47, 3), (47, 48, 3), (47, 54, 1), (44, 48, 1), (48, 49, 4), (48, 50, 10), (50, 51, 1),
        (50, 89, 6), (50, 90, 2), (47, 51, 6), (51, 52, 4), (52, 53, 1), (52, 91, 3), (53, 54, 1), (53, 59, 4),
        (54, 55, 3), (41, 55, 5), (55, 56, 1), (56, 57, 3), (56, 59, 2), (59, 60, 2), (60, 61, 1), (60, 64, 2),
        (61, 58, 6), (61, 62, 2), (62, 63, 1), (62, 64, 2), (63, 67, 2), (63, 69, 2), (58, 69, 7), (69, 70, 1),
        (70, 71, 1), (37, 70, 7), (70, 73, 3), (73, 72, 1), (73, 68, 1), (68, 69, 2), (67, 68, 1), (66, 67, 3),
        (65, 66, 1), (65, 77, 5), (64, 65, 3), (52, 64, 4), (65, 92, 2), (66, 76, 3), (67, 76, 1), (68, 74, 1),
        (74, 75, 2), (74, 76, 1), (74, 78, 2), (76, 77, 2), (77, 78, 1), (78, 79, 2), (78, 80, 6), (80, 81, 1),
        (80, 82, 16), (82, 83, 5), (82, 85, 1), (83, 84, 1), (84, 85, 4), (84, 86, 6), (85, 86, 6), (85, 92, 14),
        (86, 87, 1), (86, 88, 4), (86, 89, 4), (89, 90, 6), (90, 91, 1), (91, 92, 1),
    ]

    # Not directed
    cycle = snowymontreal.optimized_solve(False, 103, edges)
    assert is_solved(edges, cycle)

    edges = [
        (0, 1, 10), (0, 2, 20), (4, 0, 12), (1, 4, 10), (1, 3, 50), (2, 3, 20), (2, 4, 33), (5, 2, 22),
        (3, 4, 5), (3, 5, 12), (4, 5, 1)
    ]

    # Directed
    cycle = snowymontreal.solve(True, 6, edges)
    assert is_solved(edges, cycle)

    edges = [
        (0, 1, 10), (0, 2, 20), (4, 0, 12), (1, 4, 10), (1, 3, 50), (2, 3, 20), (2, 4, 33), (5, 2, 22),
        (3, 4, 5), (3, 5, 12)
    ]

    # Directed
    cycle = snowymontreal.solve(True, 6, edges)
    assert is_solved(edges, cycle)

    edges = [
        (0, 3, 5), (3, 4, 9), (6, 7, 2), (7, 8, 4), (8, 5, 12), (4, 8, 3), (4, 6, 14), (4, 7, 19), (5, 2, 19),
        (2, 5, 18), (5, 1, 6), (1, 2, 3), (1, 0, 7), (1, 3, 13),
    ]

    # Directed
    cycle = snowymontreal.solve(True, 10, edges)
    assert is_solved(edges, cycle)
