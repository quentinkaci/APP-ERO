import numpy as np
from src.floyd_warshall import floyd_warshall, get_path
from src.matching import find_max_weight_matching, find_maximum_matching
from src.graph import Graph
from src.kruskal import kruskal_min_spanning_tree
import itertools

inf, min_inf = np.iinfo(int).max, np.iinfo(int).min


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def find_path(combinations, parents):
    return [get_path(parents, src, dst) for src, dst in combinations]


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
            bipartite_matrix[src][dst] = -paths_costs[negatives[src]][positives[dst]]

    min_matching = find_max_weight_matching(bipartite_matrix)
    unbalanced_node_combinations = [(negatives[src], positives[dst]) for src, dst in min_matching.items()]

    return find_path(unbalanced_node_combinations, parents)


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

    while len(unbalanced_vertices) > 0:
        combinations = itertools.combinations(unbalanced_vertices, 2)
        graph, conversion = connected_graph_undirected([(src, dst, paths_costs[src][dst]) for src, dst in combinations])

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
