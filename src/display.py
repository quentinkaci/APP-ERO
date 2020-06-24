import osmnx as ox
from snowymontreal import solve

# set log_console to true if the map doesn't download
ox.config(use_cache=True, log_console=False)


def download_city_graph(place: str):
    return ox.graph_from_place(place, network_type='drive')


def solve_city_graph(graph):
    print("edges:", list(graph.edges))

    converted_edges_list = []
    conversions = {}

    for src, dst, w in graph.edges:
        edge_length = graph.get_edge_data(src, dst)[0]["length"]
        if src not in conversions.keys():
            conversions[src] = len(conversions)
        if dst not in conversions.keys():
            conversions[dst] = len(conversions)
        converted_edges_list.append((conversions[src], conversions[dst], edge_length))

    print("converted:", converted_edges_list)
    print("number of nodes:", G.number_of_nodes())
    path = solve(False, G.number_of_nodes(), converted_edges_list)

    reconverted_path = []
    keys = list(conversions.keys())
    vals = list(conversions.values())
    for v in path:
        reconverted_path.append(keys[vals.index(v)])

    return reconverted_path


# crashes if the route isn't legal
def show_city_graph_with_route(graph, route):
    ox.plot_graph_route(graph, route, route_linewidth=6, node_size=0, bgcolor='k')





# example:

# G = download_city_graph('Piedmont, California, USA')
point = 37.858495, -122.267468
G = ox.graph_from_point(point, network_type='drive', dist=200)

route = solve_city_graph(G)
print("best path:", route)
show_city_graph_with_route(G, route)
