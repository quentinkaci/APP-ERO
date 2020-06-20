import numpy as np


def improve_labels(lu, lv, V, S, T, minSlack, val):
    for u in S:
        lu[u] -= val
    for v in V:
        if v in T:
            lv[v] += val
        else:
            minSlack[v][0] -= val


def improve_matching(Mu, Mv, T, v):
    u = T[v]
    if u in Mu:
        improve_matching(Mu, Mv, T, Mu[u])
    Mu[u], Mv[v] = v, u


def slack(lu, lv, w, u, v): return lu[u] + lv[v] - w[u][v]


def augment(Mu, Mv, minSlack, V, S, T, lu, lv, w):
    while True:
        ((val, u), v) = min([(minSlack[v], v) for v in V if v not in T])
        if val > 0:
            improve_labels(lu, lv, V, S, T, minSlack, val)
        T[v] = u
        if v in Mv:
            u1 = Mv[v]
            S[u1] = True
            for v in V:
                if v not in T and minSlack[v][0] > slack(lu, lv, w, u1, v):
                    minSlack[v] = [slack(lu, lv, w, u1, v), u1]
        else:
            improve_matching(Mu, Mv, T, v)
            break


def max_weight_matching(weights):
    w, n = np.array(weights), len(weights)
    V = range(n)
    lu, lv = w.max(axis=1), np.full(n, 0)
    Mu, Mv = {}, {}

    while len(Mu) < n:
        u0 = [u for u in V if u not in Mu][0]
        S, T = {u0: True}, {}
        minSlack = [[slack(lu, lv, w, u0, v), u0] for v in V]
        augment(Mu, Mv, minSlack, V, S, T, lu, lv, w)

    return Mu
