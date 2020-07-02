from src.graph import Graph
from src.eulerian import make as make_eulerian
from src.eulerian.make import make_eulerian_graph
from src.eulerian.cycle import find_eulerian_cycle
import osmnx as ox
import networkx as nx


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
    # Set log_console to true if the map doesn't download
    ox.config(use_cache=True, log_console=False)

    def solve_city_graph(graph, start):
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

        path = drone_solve(conversions[start], converted_edges_list)  # FIXME
        path = [invert_conversions[v] for v in path]

        return path

    # Crashes if the route isn't legal
    def show_city_graph_with_route(graph, route):
        for i in range(1, len(route) + 1):
            ox.plot_graph_route(graph, route[:i], route_linewidth=6, node_size=0, bgcolor='k')  # FIXME

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
    start = ox.get_nearest_node(G, point, method='euclidean')
    G = G.to_undirected()  # FIXME

    route = solve_city_graph(G, start)
    show_city_graph_with_route(G, route)
