import osmnx as ox
from snowymontreal import optimized_solve

# Set log_console to true if the map doesn't download
ox.config(use_cache=True, log_console=False)


def download_city_graph(place: str):
    return ox.graph_from_place(place, network_type='drive')


def solve_city_graph(graph):
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

    path = optimized_solve(False, len(conversions), converted_edges_list)
    path = [invert_conversions[v] for v in path]

    return path


# Crashes if the route isn't legal
def show_city_graph_with_route(graph, route):
    for i in range(1, len(route) + 1):
        ox.plot_graph_route(graph, route[:i], route_linewidth=6, node_size=0, bgcolor='k')


# G = download_city_graph('Piedmont, California, USA')
lat, long = float(input("Latitude of center: ")), float(input("Longitude of center: "))
if lat < -90 or lat > 90 or long < -180 or long > 180:
    raise ValueError

dist = int(input("Distance from center to boarders: "))
if dist <= 0:
    raise ValueError

point = lat, long
G = ox.graph_from_point(point, network_type='drive', dist=dist)
G = G.to_undirected()

route = solve_city_graph(G)
show_city_graph_with_route(G, route)
