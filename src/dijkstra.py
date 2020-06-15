import numpy as np

inf = np.iinfo(int).max


def build_dist(graph):
    dist = [[0 for _ in range(graph.num_vertices)] for i in range(graph.num_vertices)]
    for (src, dst, dist) in graph.edges:
        dist[src][dst] = dist
        if not graph.directed:
            dist[dst][src] = dist
    return dist


def mindistance(graph, dist, sptSet):
    min_index, mini = inf, inf
    for v in range(graph.num_vertices):
        if dist[v] < mini and not sptSet[v]:
            mini = dist[v]
            min_index = v
    return min_index


def dijkstra(graph, src, dst):
    dist = np.full(graph.num_vertices, inf)
    dist[src] = 0
    shortest_set = np.full(graph.num_vertices, False)
    parent = np.empty(graph.num_vertices, dtype=int)

    for _ in range(graph.num_vertices):
        u = mindistance(graph, dist, shortest_set)
        shortest_set[u] = True

        for v in range(graph.num_vertices):
            dist_list = build_dist(graph)
            weight = dist[u] + dist_list[u][v]
            if dist_list[u][v] > 0 and not shortest_set[v] and dist[v] > weight:
                dist[v] = weight
                parent[v] = u
    return dist[dst], parent


def path(parent, src, dst):
    if parent is None or src is None or dst is None:
        return []

    res = [dst]
    while dst != src:
        dst = parent[dst]
        res.insert(0, dst)
    return res
