import numpy as np
import itertools


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


def make_eulerian_graph(graph):

    double_dead_end_edges(graph)

    # Step 1: All possible pairs of odd nodes
    # TODO change itertools.combinations to our own function
    odd_node_pairs = itertools.combinations(graph.get_odd_vertices(), 2)

    # FIXME

    return graph
