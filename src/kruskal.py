def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])


def union(parent, rank, x, y):
    x_root = find(parent, x)
    y_root = find(parent, y)

    if rank[x_root] < rank[y_root]:
        parent[x_root] = y_root
    elif rank[x_root] > rank[y_root]:
        parent[y_root] = x_root
    else:
        parent[y_root] = x_root
        rank[x_root] += 1


def kruskal_min_spanning_tree(graph):
    res = []
    i, e = 0, 0

    edges = sorted(graph.edges.copy(), key=lambda item: item[2])
    parent, rank = [], []

    for node in range(graph.num_vertices):
        parent.append(node)
        rank.append(0)

    while e < graph.num_vertices - 1:
        u, v, w = edges[i]
        i += 1
        x, y = find(parent, u), find(parent, v)

        if x != y:
            e += 1
            res.append((u, v, w))
            union(parent, rank, x, y)

    return res
