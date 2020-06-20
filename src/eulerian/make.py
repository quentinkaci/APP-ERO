import numpy as np
import itertools
from src.floyd_warshall import floyd_warshall, get_path
from src.hungarian import max_weight_matching
from src.graph import Graph

inf = np.iinfo(int).max


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def find_weighted_unbalanced_pairings(graph, unbalanced_vertices):
    unbalanced_vertices_pairs = list(itertools.combinations(unbalanced_vertices, 2)) if not graph.directed \
        else list(itertools.permutations(unbalanced_vertices, 2))

    res = {}
    paths_costs, parents = floyd_warshall(graph)

    for src, dst in unbalanced_vertices_pairs:
        if not (src, dst) in res:
            weight, path = paths_costs[src][dst], get_path(parents, src, dst)
            res[(src, dst)] = (weight, path)
            if not graph.directed:
                res[(dst, src)] = (weight, path[::-1])

    return res


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


def find_path(combinations, weighted_pairings):
    path = []
    for pair in combinations:
        path.append(weighted_pairings[pair][1])
    return path


def find_minimum_path_directed(graph, unbalanced_vertices, weighted_pairings):
    in_deg, out_deg = graph.get_in_degrees(), graph.get_out_degrees()
    negatives, positives = [], []

    for v in unbalanced_vertices:
        delta = out_deg[v] - in_deg[v]
        diff = abs(delta)
        for _ in range(diff):
            positives.append(v) if delta > 0 else negatives.append(v)

    bipartite_matrix = np.full((len(positives), len(negatives)), inf)
    for src in range(len(negatives)):
        for dst in range(len(positives)):
            bipartite_matrix[src][dst] = -weighted_pairings[(negatives[src], positives[dst])][0]

    min_matching = max_weight_matching(bipartite_matrix)
    print(min_matching)
    unbalanced_node_combinations = []
    for src, dst in min_matching.items():
        unbalanced_node_combinations.append((negatives[src], positives[dst]))

    return find_path(unbalanced_node_combinations, weighted_pairings)


def find_minimum_path_undirected(unbalanced_vertices, weighted_pairings):
    unbalanced_pairs = all_matching(unbalanced_vertices)

    min_weight = inf
    min_path = []

    for unbalanced_pair in unbalanced_pairs:
        pair_weight = 0
        for pair in unbalanced_pair:
            pair_weight += weighted_pairings[pair][0]
        if pair_weight < min_weight:
            min_weight = pair_weight
            min_path = find_path(unbalanced_pair, weighted_pairings)

    return min_path


def add_min_path_edges(graph, paths):
    adjacency_matrix = graph.get_adjacency_matrix()
    edges_to_add = []

    for path in paths:
        for i in range(len(path) - 1):
            src, dst = path[i], path[i + 1]
            edges_to_add.append((src, dst, adjacency_matrix[src][dst]))

    graph.add_edges(edges_to_add)


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


def make_eulerian_graph(graph):
    """if not graph.directed:
        min_spanning_tree = kruskal_min_spanning_tree(graph)
        graph = Graph(graph.num_vertices, min_spanning_tree)"""
    double_dead_end_edges(graph)

    unbalanced_vertices = graph.get_unbalanced_vertices()
    weighted_pairings = find_weighted_unbalanced_pairings(graph, unbalanced_vertices)

    min_path = find_minimum_path_directed(graph, unbalanced_vertices, weighted_pairings) if graph.directed \
        else find_minimum_path_undirected(unbalanced_vertices, weighted_pairings)
    add_min_path_edges(graph, min_path)

    return graph
