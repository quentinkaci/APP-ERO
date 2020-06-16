import numpy as np
import itertools
from src.dijkstra import dijkstra


def hierholzer_cycle(graph):
    if graph.num_edges == 0:
        return []

    start = np.random.choice(np.arange(graph.num_vertices))
    cycle = [start]  # start somewhere randomly

    edges = graph.edges.copy()
    while True:
        rest = []
        for src, dst, dist in edges:
            if cycle[-1] == src:
                cycle.append(dst)
            elif not graph.directed and cycle[-1] == dst:
                cycle.append(src)
            else:
                rest.append((src, dst, dist))
        if not rest:
            return cycle
        edges = rest
        if cycle[0] == cycle[-1]:
            for src, dst, _ in edges:
                if src in cycle:
                    idx = cycle.index(src)
                    cycle = cycle[idx:-1] + cycle[0:idx + 1]
                    break


def find_eulerian_cycle(graph):
    return hierholzer_cycle(graph)


def double_dead_end_edges(graph):
    single_vertices = graph.get_single_vertices()

    edges_to_double = []
    for v in single_vertices:
        for src, dst, dist in graph.edges:
            if v in (src, dst):
                edges_to_double.append((src, dst, dist))

    graph.add_edges(list(set(edges_to_double)))


def find_weighted_odd_pairings(graph):
    # TODO change itertools.combinations to our own function
    odd_node_pairs = list(itertools.combinations(graph.get_odd_vertices(), 2)) if not graph.directed \
        else list(itertools.permutations(graph.get_odd_vertices(), 2))
    res = {}

    for src, dst in odd_node_pairs:
        if not (src, dst) in res:
            weight, path = dijkstra(graph, src, dst)

            res[(src, dst)] = (weight, path)
            if not graph.directed:  # FIXME
                res[(dst, src)] = (weight, path[::-1])

    return res


def make_eulerian_graph(graph):
    double_dead_end_edges(graph)

    weighted_pairings = find_weighted_odd_pairings(graph)

    # FIXME

    return graph
