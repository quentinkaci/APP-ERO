import numpy as np


class Graph:
    def __init__(self, num_vertices=0, edges=None, directed=False):
        if edges is None:
            edges = []
        self.edges = edges.copy()
        self.num_vertices = num_vertices
        self.num_edges = len(edges)
        self.directed = directed

    def get_out_degrees(self):
        deg = np.full(self.num_vertices, 0)
        for src, dst, _ in self.edges:
            deg[src] += 1
            if not self.directed:
                deg[dst] += 1
        return deg

    def get_in_degrees(self):
        deg = np.full(self.num_vertices, 0)
        for src, dst, _ in self.edges:
            deg[dst] += 1
            if not self.directed:
                deg[src] += 1
        return deg

    def get_degrees(self):
        deg = np.full(self.num_vertices, 0)
        for src, dst, _ in self.edges:
            deg[src] += 1
            deg[dst] += 1
        return deg

    def get_odd_vertices(self):
        deg = self.get_degrees()
        return [v for v in range(self.num_vertices) if deg[v] % 2 == 1]

    def get_unbalanced_vertices(self):
        res = []

        if self.directed:
            in_deg = self.get_in_degrees()
            out_deg = self.get_out_degrees()

            for vertex in range(self.num_vertices):
                if out_deg[vertex] - in_deg[vertex] != 0:
                    res.append(vertex)
        else:
            res = self.get_odd_vertices()

        return res

    def get_single_vertices(self):
        deg = self.get_degrees()
        return [v for v in range(self.num_vertices) if deg[v] == 1]

    def is_eulerian(self):
        # Forgetting if the graph is not edge connected

        if self.directed and (self.get_out_degrees() != self.get_in_degrees()).all():
            return False

        return len(self.get_odd_vertices()) == 0

    def add_edges(self, edges_to_add):
        self.edges.extend(edges_to_add)
        self.num_edges = len(self.edges)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.num_edges += 1

    def get_adjacency_matrix(self):
        matrix = np.full((self.num_vertices, self.num_vertices), 0)
        for src, dst, dist in self.edges:
            matrix[src][dst] = dist
            if not self.directed:
                matrix[dst][src] = dist
        return matrix

    def get_adjacency_list(self):
        res = [[] for _ in range(self.num_vertices)]
        for src, dst, _ in self.edges:
            res[src].append(dst)
            if not self.directed:
                res[dst].append(src)
        return res
