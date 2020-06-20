import numpy as np
from src.floyd_warshall import floyd_warshall, get_path
from src.hungarian import max_weight_matching

inf = np.iinfo(int).max
min_inf = np.iinfo(int).min


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def all_matching_undirected(unbalanced_vertices):
    for node in unbalanced_vertices[1:]:
        pair = unbalanced_vertices[0], node
        rest = [n for n in unbalanced_vertices if n not in pair]
        if rest:
            for tail in all_matching_undirected(rest):
                yield [pair] + tail
        else:
            yield [pair]


def all_matching(unbalanced_vertices):
    return [x for x in all_matching_undirected(unbalanced_vertices)]


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

    min_matching = max_weight_matching(bipartite_matrix)
    unbalanced_node_combinations = [(negatives[src], positives[dst]) for src, dst in min_matching.items()]

    return find_path(unbalanced_node_combinations, parents)


def find_minimum_path_undirected(unbalanced_vertices, paths_costs, parents):
    unbalanced_pairs = all_matching(unbalanced_vertices)

    min_weight = inf
    min_path = []

    for unbalanced_pair in unbalanced_pairs:
        pair_weight = 0
        for src, dst in unbalanced_pair:
            pair_weight += paths_costs[src][dst]
        if pair_weight < min_weight:
            min_weight = pair_weight
            min_path = find_path(unbalanced_pair, parents)

    return min_path


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


"""
def connected_graph_undirected(edges):
    conversion = {}
    for edge, dist in edges.items():
        src, dst = edge[0], edge[1]
        if src not in conversion.keys():
            conversion[src] = len(conversion)
        if dst not in conversion.keys():
            conversion[dst] = len(conversion)

    graph = Graph(len(conversion))
    for edge, dist in edges.items():
        graph.add_edge([conversion[edge[0]], conversion[edge[1]], dist[0]])

    return graph, {value: key for (key, value) in conversion.items()}
"""


def make_eulerian_graph(graph):
    if not graph.directed:
        double_dead_end_edges(graph)

    return add_min_path_edges(graph, find_minimum_path(graph))
