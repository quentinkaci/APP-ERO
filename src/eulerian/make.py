import numpy as np
import itertools
from src.dijkstra import dijkstra

inf = np.iinfo(int).max


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def find_weighted_odd_pairings(graph):
    # TODO change itertools.combinations and itertools.permutations to our own function
    odd_node_pairs = list(itertools.combinations(graph.get_odd_vertices(), 2)) if not graph.directed \
        else list(itertools.permutations(graph.get_odd_vertices(), 2))
    res = {}

    for src, dst in odd_node_pairs:
        if not (src, dst) in res:
            weight, path = dijkstra(graph, src, dst)

            res[(src, dst)] = (weight, path)
            if not graph.directed:  # FIXME maybe a bug
                res[(dst, src)] = (weight, path[::-1])

    return res


# TODO change this function by removing yield
def all_possible_pairs(odd_nodes):
    for node in odd_nodes[1:]:
        pair = odd_nodes[0], node
        rest = [n for n in odd_nodes if n not in pair]
        if rest:
            for tail in all_possible_pairs(rest):
                yield [pair] + tail
        else:
            yield [pair]


def find_minimum_path(odd_node_pairs, weighted_pairings):
    min_weight = inf
    min_path = []

    for odd_node_pair in odd_node_pairs:
        pair_weight = 0
        for pair in odd_node_pair:
            pair_weight += weighted_pairings[pair][0]
        if pair_weight < min_weight:
            min_weight = pair_weight
            path = []
            for pair in odd_node_pair:
                path.append(weighted_pairings[pair][1])
            min_path = path

    return min_path


def add_shortest_path_edges(graph, paths):
    adjacency_matrix = graph.get_adjacency_matrix()
    edges_to_add = []
    for path in paths:
        for i in range(len(path) - 1):
            src, dst = path[i], path[i + 1]
            edges_to_add.append((src, dst, adjacency_matrix[src][dst]))
    graph.add_edges(edges_to_add)


def make_eulerian_graph(graph):
    double_dead_end_edges(graph)

    weighted_pairings = find_weighted_odd_pairings(graph)

    odd_node_pairs = [x for x in all_possible_pairs(graph.get_odd_vertices())]

    min_path = find_minimum_path(odd_node_pairs, weighted_pairings)
    add_shortest_path_edges(graph, min_path)

    return graph
