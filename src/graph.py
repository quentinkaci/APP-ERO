class Graph:
    def __init__(self, num_vertices=0, edges=None, directed=False):
        if edges is None:
            edges = []
        self.edges = edges.copy()
        self.num_vertices = num_vertices
        self.num_edges = len(edges)
        self.directed = directed

    def get_odd_vertices(self):
        deg = [0] * self.num_vertices
        for src, dst, _ in self.edges:
            deg[src] += 1
            if self.directed:
                deg[dst] += 1
        return [a for a in range(self.num_vertices) if not deg[a] % 2]

    def is_eulerian(self):
        # Forgetting if the graph is not edge connected
        return len(self.get_odd_vertices()) == 0
