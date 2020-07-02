from src.floyd_warshall import floyd_warshall, get_path
from src.graph import Graph
from src.kruskal import kruskal_min_spanning_tree
from src.matching import find_maximum_matching
import numpy as np
import scipy.optimize
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

    row_ind, col_ind = scipy.optimize.linear_sum_assignment(bipartite_matrix)
    min_matching = [(negatives[row_ind[i]], positives[col_ind[i]]) for i in range(len(negatives))]

    return find_path(min_matching, parents)


def connected_graph_undirected(edges):
    conversion = {}
    for src, dst, dist in edges:
        if src not in conversion.keys():
            conversion[src] = len(conversion)
        if dst not in conversion.keys():
            conversion[dst] = len(conversion)

    graph = Graph(len(conversion))
    for src, dst, dist in edges:
        graph.add_edge([conversion[src], conversion[dst], dist])

    return graph, {value: key for (key, value) in conversion.items()}


def find_minimum_path_undirected(unbalanced_vertices, paths_costs, parents):
    min_matching = []

    if optimized:
        nx_graph = nx.Graph()
        combinations = itertools.combinations(unbalanced_vertices, 2)
        for src, dst in combinations:
            nx_graph.add_edge(src, dst, weight=-paths_costs[src][dst])

        min_matching = list(nx.max_weight_matching(nx_graph, True))
    else:
        while len(unbalanced_vertices) > 0:
            combinations = itertools.combinations(unbalanced_vertices, 2)
            graph, conversion = connected_graph_undirected([(src, dst, paths_costs[src][dst])
                                                            for src, dst in combinations])

            min_spanning_tree = [(src, dst) for src, dst, _ in kruskal_min_spanning_tree(graph)]
            matching = find_maximum_matching(graph.num_vertices, min_spanning_tree)
            converted_matching = [(conversion[src], conversion[dst]) for src, dst in matching]
            min_matching.extend(converted_matching)

            for src, dst in converted_matching:
                unbalanced_vertices.remove(src)
                unbalanced_vertices.remove(dst)

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
