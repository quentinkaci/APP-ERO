import numpy as np

inf = np.iinfo(int).max


def xor_edges(edges1, edges2):
    res = edges1.copy()
    for (s, d) in edges2:
        if (s, d) in res:
            res.remove((s, d))
        elif (d, s) in res:
            res.remove((d, s))
        else:
            res.append((s, d))

    return res


def find_exposed_vertices(n, matching):
    res = []
    for v in range(n):
        found = False
        for (s, d) in matching:
            if v == s or v == d:
                found = True
                break
        if not found:
            res.append(v)
    return res


def is_edges_coupled(s, d, matching):
    return (s, d) in matching or (d, s) in matching


def find_augmenting_path(n, edges, matching):
    succ = [[] for _ in range(n)]
    for (s, d) in edges:
        if d not in succ[s]:
            succ[s].append(d)
            succ[d].append(s)

    def dfs(src, dst, res, even=True):
        if src == dst:
            return True

        found = False
        for d in succ[src]:
            if not d in res:
                if even and is_edges_coupled(src, d, matching):
                    continue
                if not even and not is_edges_coupled(src, d, matching):
                    continue

                found = True
                res.append(d)
                if dfs(d, dst, res, not even):
                    return True
                res.remove(d)

        if not found:
            return False

    exposed = find_exposed_vertices(n, matching)
    len_exposed = len(exposed)
    for i in range(len_exposed):
        for j in range(i + 1, len_exposed):
            src = exposed[i]
            dst = exposed[j]

            res = [src]
            if dfs(src, dst, res):
                return res

    return None


def path_to_pairs(path):
    res = []
    for i in range(len(path) - 1):
        res.append((path[i], path[i + 1]))
    return res


def find_maximum_matching(n, edges):
    res = []
    tmp = find_augmenting_path(n, edges, res)
    while tmp is not None:
        res = xor_edges(res, path_to_pairs(tmp))
        tmp = find_augmenting_path(n, edges, res)
    return res


def find(parent, i):
    while parent[i] != i:
        i = parent[i]
    return i


def union(parent, position, x, y):
    x_parent, y_parent = find(parent, x), find(parent, y)

    if position[x_parent] < position[y_parent]:
        parent[x_parent] = y_parent
        return
    elif position[x_parent] > position[y_parent]:
        parent[y_parent] = x_parent
        return

    parent[y_parent] = x_parent
    position[x_parent] += 1


# We use the Union-Find algorithm to detect if there is a cycle
def kruskal_min_spanning_tree(graph):
    res = []
    i, num_edges = 0, 0

    parent, position = np.arange(graph.num_vertices), np.full(graph.num_vertices, 0)
    sorted_edges = sorted(graph.edges.copy(), key=lambda item: item[2])

    while num_edges < graph.num_vertices - 1:
        src, dst, dist = sorted_edges[i]
        src_parent, dst_parent = find(parent, src), find(parent, dst)

        if src_parent != dst_parent:  # There is a cycle
            num_edges += 1
            res.append((src, dst, dist))
            union(parent, position, src_parent, dst_parent)

        i += 1

    return res


def floyd_warshall(graph):
    M = np.full((graph.num_vertices, graph.num_vertices), inf, dtype=int)
    D = np.full((graph.num_vertices, graph.num_vertices), np.nan, dtype=int)

    for s, d, w in graph.edges:
        M[s][d] = w
        D[s][d] = s
        if not graph.directed:
            M[d][s] = w
            D[d][s] = d
    for i in range(graph.num_vertices):
        M[i][i] = 0
        D[i][i] = i

    for k in range(graph.num_vertices):
        for i in range(graph.num_vertices):
            for j in range(graph.num_vertices):
                old = M[i][j]
                new = M[i][k] + M[k][j] if M[i][k] != inf and M[k][j] != inf else inf
                M[i][j] = min(M[i][j], new)
                if old != M[i][j]:
                    D[i][j] = D[k][j]

    return M, D


def get_path(D, source, destination):
    if D[source][destination] == np.nan:
        return []

    res = [destination]
    while destination != source:
        destination = D[source][destination]
        res.insert(0, destination)

    return res
