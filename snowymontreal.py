from src.graph import Graph
from src.eulerian import find_eulerian_cycle, make_eulerian_graph


def solve(is_oriented, num_vertices, edge_list):
    graph = Graph(num_vertices, edge_list, is_oriented)

    if graph.is_eulerian():
        return find_eulerian_cycle(graph)
    else:
        return find_eulerian_cycle(make_eulerian_graph(graph))
