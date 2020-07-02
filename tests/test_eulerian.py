from eulerian.cycle import find_eulerian_cycle
from eulerian.make import make_eulerian_graph
from graph import Graph
from tests.tools import is_eulerian_cycle


def test_find_eulerian_cycle():
    edges = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 2, 1),
             (3, 1, 1), (4, 1, 1), (3, 2, 1), (2, 4, 1), (4, 3, 1)]
    graph = Graph(5, edges)

    cycle = find_eulerian_cycle(graph)
    assert is_eulerian_cycle(edges, cycle[:-1])

    edges = [(0, 1, 1), (1, 2, 1), (2, 4, 1), (2, 3, 1), (3, 2, 1), (4, 0, 1)]
    graph = Graph(5, edges, True)

    cycle = find_eulerian_cycle(graph)
    assert is_eulerian_cycle(edges, cycle[:-1])


def test_make_eulerian_graph():
    edges = [
        (0, 1, 1), (1, 2, 1), (2, 3, 1), (2, 24, 6), (1, 3, 1), (1, 23, 7), (3, 4, 3), (4, 5, 1), (4, 25, 6),
        (5, 6, 1), (5, 7, 1), (7, 8, 12), (7, 25, 7), (8, 9, 5), (8, 18, 4), (9, 10, 1), (9, 18, 1), (9, 11, 2),
        (11, 12, 4), (11, 17, 1), (12, 13, 1), (12, 14, 1), (12, 15, 4), (16, 17, 8), (17, 18, 1), (17, 19, 1),
        (18, 19, 1), (19, 20, 5), (20, 21, 1), (21, 22, 1), (21, 23, 5), (20, 24, 4), (23, 24, 3), (24, 25, 1),
        (25, 26, 1)
    ]

    graph = Graph(27, edges)
    graph = make_eulerian_graph(graph)

    assert graph.is_eulerian()

    edges = [
        (0, 3, 5), (3, 4, 9), (6, 7, 2), (7, 8, 4), (8, 5, 12), (4, 8, 3), (4, 6, 14), (4, 7, 19), (5, 2, 19),
        (2, 5, 18), (5, 1, 6), (1, 2, 3), (1, 0, 7), (1, 3, 13),
    ]

    graph = Graph(10, edges, True)
    graph = make_eulerian_graph(graph)

    assert graph.is_eulerian()
