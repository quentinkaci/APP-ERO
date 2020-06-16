import numpy as np

inf = np.iinfo(int).max


def min_distance(graph, dist, shortest_set):
    min_index, mini = -1, inf
    for v in range(graph.num_vertices):
        if dist[v] < mini and not shortest_set[v]:
            mini = dist[v]
            min_index = v
    return min_index


def path(parent, src, dst):
    if parent is None or src is None or dst is None:
        return []

    res = [dst]
    while dst != src:
        dst = parent[dst]
        res.insert(0, dst)
    return res


def dijkstra(graph, src, dst):
    dist = np.full(graph.num_vertices, inf)
    dist[src] = 0
    shortest_set = np.full(graph.num_vertices, False)
    parent = np.empty(graph.num_vertices, dtype=int)

    matrix = graph.get_adjacency_matrix()

    for _ in range(graph.num_vertices):
        u = min_distance(graph, dist, shortest_set)
        shortest_set[u] = True

        for v in range(graph.num_vertices):
            weight = dist[u] + matrix[u][v]
            if matrix[u][v] > 0 and not shortest_set[v] and dist[v] > weight:
                dist[v] = weight
                parent[v] = u

    return dist[dst], path(parent, src, dst)
