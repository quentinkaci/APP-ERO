from src.graph import Graph
import src.eulerian.make as make_eulerian
from src.eulerian.make import make_eulerian_graph
from src.eulerian.cycle import find_eulerian_cycle


def optimized_solve(is_oriented, num_vertices, edge_list):
    make_eulerian.optimized = True
    return solve(is_oriented, num_vertices, edge_list)


def solve(is_oriented, num_vertices, edge_list):
    graph = Graph(num_vertices, edge_list, is_oriented)

    try:
        if graph.is_eulerian():
            return find_eulerian_cycle(graph)
        else:
            return find_eulerian_cycle(make_eulerian_graph(graph))
    except:
        return []
