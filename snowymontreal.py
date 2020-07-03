from src.graph import Graph
from src.eulerian import make as make_eulerian
from src.eulerian.make import make_eulerian_graph
from src.eulerian.cycle import find_eulerian_cycle
import osmnx as ox
from matplotlib import pyplot as plt
import networkx as nx
import sys


def optimized_solve(is_oriented, num_vertices, edge_list):
    make_eulerian.optimized = True
    return solve(is_oriented, num_vertices, edge_list)


def solve(is_oriented, num_vertices, edge_list):
    graph = Graph(num_vertices, edge_list, is_oriented)

    try:
        if graph.is_eulerian():
            return find_eulerian_cycle(graph)
        else:
            return find_eulerian_cycle(make_eulerian_graph(graph))
    except:
        return []


def snow_plow_solve(start, num_vertices, edge_list):
    graph = Graph(num_vertices, edge_list, True)

    try:
        if graph.is_eulerian():
            return find_eulerian_cycle(graph, start)
        else:
            return find_eulerian_cycle(make_eulerian_graph(graph), start)
    except:
        return []


def drone_solve(start, edge_list):
    nx_graph = nx.Graph()
    nx_graph.add_weighted_edges_from(edge_list)

    if nx.is_eulerian(nx_graph):
        return nx.eulerian_circuit(nx_graph, source=start)

    circuit = nx.eulerian_circuit(nx.eulerize(nx_graph), source=start)
    res = [src for src, _ in circuit]
    res.append(start)

    return res


if __name__ == "__main__":
    ox.config(use_cache=True, log_console=False)

    def solve_city_graph(graph, start, used):
        converted_edges_list = []
        conversions = {}

        for src, dst, w in graph.edges:
            edge_length = graph.get_edge_data(src, dst)[0]["length"]
            if src not in conversions.keys():
                conversions[src] = len(conversions)
            if dst not in conversions.keys():
                conversions[dst] = len(conversions)
            converted_edges_list.append((conversions[src], conversions[dst], edge_length))

        invert_conversions = {value: key for (key, value) in conversions.items()}

        if used == "drone":
            path = drone_solve(conversions[start], converted_edges_list)
        else:
            path = snow_plow_solve(conversions[start], len(conversions), converted_edges_list)

        path = [invert_conversions[v] for v in path]

        return path

    def show_city_graph_with_route(graph, route):
        for i in range(1, len(route) + 1):
            ox.plot_graph_route(graph, route[:i], route_linewidth=6, node_size=0, bgcolor='k')
            if "--no-interactive" not in sys.argv:
                plt.pause(0.5)
                plt.close()


    if "--no-interactive" not in sys.argv:
        plt.ion()

    used = ""
    while used not in ("drone", "snow plow"):
        used = input("Type \"drone\" or \"snow plow\" depending on what you want to use: ")

    lat, long = float(input("Latitude of " + used + ": ")), float(input("Longitude of " + used + ": "))
    if lat < -90 or lat > 90 or long < -180 or long > 180:
        raise ValueError

    dist = int(input("Radius for " + used + " to cover: "))
    if dist <= 0:
        raise ValueError

    point = lat, long
    G = ox.graph_from_point(point, network_type='drive', dist=dist)

    edges, i = [(src, dst) for src, dst, _ in G.edges], 0
    for src, dst in edges:
        i += 1
        if (dst, src) in edges[i:]:
            try:
                G.remove_edge(dst, src)
            except:
                continue

    if used == "snow plow":
        edges_to_add = [(dst, src, w) for src, dst, w in G.edges]
        for src, dst, w in edges_to_add:
            G.add_edge(src, dst, length=w)
    else:
        G = G.to_undirected()

    start = ox.get_nearest_node(G, point, method='euclidean')
    route = solve_city_graph(G, start, used)

    show_city_graph_with_route(G, route)
