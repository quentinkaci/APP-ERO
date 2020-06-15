def adjacency_list(graph):
    succ = [[] for i in range(graph.num_vertices)]

    for (src, dst, dist) in graph.edges:
        succ[src].append((dst, dist))
        if not graph.directed:
            succ[dst].append((src, dist))
    return succ

class Graph:
    def __init__(self, num_vertices=0, edges=None, directed=False):
        if edges is None:
            edges = []
        self.edges = edges.copy()
        self.num_vertices = num_vertices
        self.num_edges = len(edges)
        self.directed = directed
        self.adjacency_list = adjacency_list(self)

    def get_odd_vertices(self):
        deg = [0] * self.num_vertices
        for src, dst, _ in self.edges:
            deg[src] += 1
            deg[dst] += 1
        return [v for v in range(self.num_vertices) if not deg[v] % 2]

    def is_eulerian(self):
        # Forgetting if the graph is not edge connected
        return len(self.get_odd_vertices()) == 0

