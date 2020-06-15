import numpy as np


def hierholzer_cycle(graph):
    if graph.num_edges == 0:
        return []

    start = np.random.choice(np.arange(graph.num_vertices))
    cycle = [start]  # start somewhere randomly

    edges = graph.edges.copy()
    while True:
        rest = []
        for src, dst, _ in edges:
            if cycle[-1] == src:
                cycle.append(dst)
            elif not graph.directed and cycle[-1] == dst:
                cycle.append(src)
            else:
                rest.append((src, dst))
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
    for i in range(2000):
        path = hierholzer_cycle(graph)
        if len(path) == graph.num_edges + 1:
            return path
    return []


def make_eulerian_graph(graph):
    # FIXME
    return graph
