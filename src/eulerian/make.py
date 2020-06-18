import numpy as np
import itertools
from src.floyd_warshall import floyd_warshall, get_path

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
    # TODO change itertools.combinations and itertools.permutations to our own function
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


# TODO change this function by removing yield
def all_matching_undirected(unbalanced_vertices):
    for node in unbalanced_vertices[1:]:
        pair = unbalanced_vertices[0], node
        rest = [n for n in unbalanced_vertices if n not in pair]
        if rest:
            for tail in all_matching_undirected(rest):
                yield [pair] + tail
        else:
            yield [pair]


def all_matching_directed(graph, unbalanced_vertices):
    in_deg, out_deg = graph.get_in_degrees(), graph.get_out_degrees()
    negatives, positives = [], []

    for v in unbalanced_vertices:
        delta = out_deg[v] - in_deg[v]
        diff = abs(delta)
        for _ in range(diff):
            positives.append(v) if delta > 0 else negatives.append(v)

    combinations = np.array(np.meshgrid(negatives, positives)).T.reshape(len(positives), len(positives), 2)
    combinations_tuple = []
    for combination in combinations:
        combination_tuple = []
        for pair in combination:
            combination_tuple.append((pair[0], pair[1]))
        combinations_tuple.append(combination_tuple)
    combinations = itertools.product(*combinations_tuple)

    res = []
    for combination in combinations:
        used = np.full(graph.num_vertices, False)
        for pair in combination:
            used[pair[0]] = True
            used[pair[1]] = True
        to_add = True
        for v in unbalanced_vertices:
            to_add &= used[v]
        if to_add:
            res.append([x for x in combination])
    return res


def all_matching(graph, unbalanced_vertices):
    return all_matching_directed(graph, unbalanced_vertices) if graph.directed \
        else [x for x in all_matching_undirected(unbalanced_vertices)]


def find_minimum_path(unbalanced_pairs, weighted_pairings):
    min_weight = inf
    min_path = []

    for unbalanced_pair in unbalanced_pairs:
        pair_weight = 0
        for pair in unbalanced_pair:
            pair_weight += weighted_pairings[pair][0]
        if pair_weight < min_weight:
            min_weight = pair_weight
            path = []
            for pair in unbalanced_pair:
                path.append(weighted_pairings[pair][1])
            min_path = path

    return min_path


def add_min_path_edges(graph, paths):
    adjacency_matrix = graph.get_adjacency_matrix()
    edges_to_add = []

    for path in paths:
        for i in range(len(path) - 1):
            src, dst = path[i], path[i + 1]
            edges_to_add.append((src, dst, adjacency_matrix[src][dst]))

    graph.add_edges(edges_to_add)


def make_eulerian_graph(graph):
    double_dead_end_edges(graph)

    unbalanced_vertices = graph.get_unbalanced_vertices()
    weighted_pairings = find_weighted_unbalanced_pairings(graph, unbalanced_vertices)
    unbalanced_node_combinations = all_matching(graph, unbalanced_vertices)

    min_path = find_minimum_path(unbalanced_node_combinations, weighted_pairings)
    add_min_path_edges(graph, min_path)

    return graph
