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
