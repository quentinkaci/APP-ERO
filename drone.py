import numpy as np

inf = np.iinfo(int).max


def adjacency_list(n, edges):
    succ = [[] for i in range(n)]

    for (src, dst, dist) in edges:
        succ[src].append((dst, dist))
        succ[dst].append((src, dist))

    return succ


# TODO change this function to adapt Dijkstra to cover all edges
def shortest_path(n, succ, src, dst):
    dist = np.full(n, inf)
    dist[src] = 0
    parent = np.empty(n, dtype=int)

    vertices_set = set()
    vertices_set.add((0, src))

    while len(vertices_set) != 0:
        _, u = vertices_set.pop()

        for v, weight in succ[u]:
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                parent[v] = u
                vertices_set.add((dist[v], v))

    return dist[dst], parent


def path(parent, src, dst):
    if parent is None or src is None or dst is None:
        return []

    res = [dst]
    while dst != src:
        dst = parent[dst]
        res.insert(0, dst)
    res.append(src)

    return res


def solve(n, edges):
    succ = adjacency_list(n, edges)

    min_cycle = inf
    min_parent, min_src, min_dst = None, None, None

    num_edges = len(edges)
    for i in range(num_edges):
        src, dst, weight = edges[i]

        # Remove edge
        succ[src].remove((dst, weight))
        succ[dst].remove((src, weight))

        dist, parent = shortest_path(n, succ, src, dst)
        if dist + weight < min_cycle:
            min_cycle = dist + weight
            min_parent, min_src, min_dst = parent, src, dst

        # Restore edge
        succ[src].append((dst, weight))
        succ[dst].append((src, weight))

    return path(min_parent, min_src, min_dst)
