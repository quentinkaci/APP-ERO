def remove_weights(edges):
    res = []
    for src, dst, _ in edges:
        res.append((src, dst))
    return res


def nedge(a, b):
    return (a, b) if a < b else (b, a)


def is_eulerian_cycle(edges, cycle):
    edges = remove_weights(edges)
    if len(edges) != len(cycle):
        return False
    if len(edges) == 0:
        return True
    eset = {}
    for (a, b) in edges:
        s = nedge(a, b)
        if s in eset:
            eset[s] += 1
        else:
            eset[s] = 1
    for (a, b) in zip(cycle, cycle[1:] + cycle[0:1]):
        s = nedge(a, b)
        if s in eset and eset[s] > 0:
            eset[s] -= 1
        else:
            return False
    for val in eset.values():
        if val != 0:
            return False
    return True


def is_solved(edges, cycle):
    edges = remove_weights(edges)

    for node in range(len(cycle) - 1):
        src, dst = cycle[node], cycle[node + 1]
        if not (src, dst) in edges and not (dst, src) in edges:
            continue

        try:
            edges.remove((src, dst))
        except:
            edges.remove((dst, src))

    return len(edges) == 0
