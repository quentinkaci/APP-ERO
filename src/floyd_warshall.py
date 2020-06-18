import numpy as np

inf = np.iinfo(int).max


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
