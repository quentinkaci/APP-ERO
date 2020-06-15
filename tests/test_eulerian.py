from src.eulerian import find_eulerian_cycle
from src.graph import Graph


def test_find_eulerian_cycle():
    edges = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 2, 1),
             (3, 1, 1), (4, 1, 1), (3, 2, 1), (2, 4, 1), (4, 3, 1)]
    graph = Graph(5, edges)
    print(find_eulerian_cycle(graph))

    edges = [(0, 1, 1), (1, 2, 1), (2, 4, 1), (2, 3, 1), (3, 2, 1), (4, 0, 1)]
    graph = Graph(5, edges, True)
    print(find_eulerian_cycle(graph))


test_find_eulerian_cycle()
