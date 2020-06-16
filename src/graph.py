import numpy as np


class Graph:
    def __init__(self, num_vertices=0, edges=None, directed=False):
        if edges is None:
            edges = []
        self.edges = edges.copy()
        self.num_vertices = num_vertices
        self.num_edges = len(edges)
        self.directed = directed

    def get_degrees(self):
        deg = [0] * self.num_vertices
        for src, dst, _ in self.edges:
            deg[src] += 1
            deg[dst] += 1
        return deg

    def get_odd_vertices(self):
        deg = self.get_degrees()
        return [v for v in range(self.num_vertices) if deg[v] % 2 == 1]

    def get_single_vertices(self):
        deg = self.get_degrees()
        return [v for v in range(self.num_vertices) if deg[v] == 1]

    def is_eulerian(self):
        # Forgetting if the graph is not edge connected
        return len(self.get_odd_vertices()) == 0

    def add_edges(self, edges_to_add):
        self.edges.extend(edges_to_add)

    def get_adjacency_matrix(self):
        matrix = np.full((self.num_vertices, self.num_vertices), 0)
        for src, dst, dist in self.edges:
            matrix[src][dst] = dist
            if not self.directed:
                matrix[dst][src] = dist
        return matrix
