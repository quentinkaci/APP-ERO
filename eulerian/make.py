import numpy as np
from floyd_warshall import floyd_warshall, get_path
from scipy.optimize import linear_sum_assignment
import itertools
import networkx as nx

inf, min_inf = np.iinfo(int).max, np.iinfo(int).min

optimized = False


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def find_path(matching, parents):
    return [get_path(parents, src, dst) for src, dst in matching]


def find_minimum_path_directed(graph, unbalanced_vertices, paths_costs, parents):
    in_deg, out_deg = graph.get_in_degrees(), graph.get_out_degrees()
    negatives, positives = [], []

    for v in unbalanced_vertices:
        delta = out_deg[v] - in_deg[v]
        diff = abs(delta)
        for _ in range(diff):
            positives.append(v) if delta > 0 else negatives.append(v)

    bipartite_matrix = np.full((len(positives), len(negatives)), min_inf)
    for src in range(len(negatives)):
        for dst in range(len(positives)):
            bipartite_matrix[src][dst] = paths_costs[negatives[src]][positives[dst]]

    row_ind, col_ind = linear_sum_assignment(bipartite_matrix)
    min_matching = [(negatives[row_ind[i]], positives[col_ind[i]]) for i in range(len(negatives))]

    return find_path(min_matching, parents)


def all_matching(unbalanced_vertices):
    for vertex in unbalanced_vertices[1:]:
        pair = unbalanced_vertices[0], vertex
        rest = [n for n in unbalanced_vertices if n not in pair]
        if rest:
            for tail in all_matching(rest):
                yield [pair] + tail
        else:
            yield [pair]


def find_minimum_path_undirected(unbalanced_vertices, paths_costs, parents):
    if optimized:
        nx_graph = nx.Graph()
        combinations = itertools.combinations(unbalanced_vertices, 2)
        for src, dst in combinations:
            nx_graph.add_edge(src, dst, weight=-paths_costs[src][dst])

        min_matching = list(nx.max_weight_matching(nx_graph, True))
    else:
        all_possible_matching = [x for x in all_matching(unbalanced_vertices)]

        min_weight = inf
        min_matching = []

        for matching in all_possible_matching:
            pair_weight = 0
            for src, dst in matching:
                pair_weight += paths_costs[src][dst]
            if pair_weight < min_weight:
                min_weight = pair_weight
                min_matching = matching

    return find_path(min_matching, parents)


def find_minimum_path(graph):
    unbalanced_vertices = graph.get_unbalanced_vertices()
    paths_costs, parents = floyd_warshall(graph)

    return find_minimum_path_directed(graph, unbalanced_vertices, paths_costs, parents) if graph.directed \
        else find_minimum_path_undirected(unbalanced_vertices, paths_costs, parents)


def add_min_path_edges(graph, paths):
    adjacency_matrix = graph.get_adjacency_matrix()
    edges_to_add = []

    for path in paths:
        for i in range(len(path) - 1):
            src, dst = path[i], path[i + 1]
            edges_to_add.append((src, dst, adjacency_matrix[src][dst]))

    graph.add_edges(edges_to_add)
    return graph


def make_eulerian_graph(graph):
    if not graph.directed:
        double_dead_end_edges(graph)

    return add_min_path_edges(graph, find_minimum_path(graph))
