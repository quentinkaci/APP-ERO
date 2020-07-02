def hierholzer_cycle(graph, start):
    if graph.num_edges == 0:
        return []

    adj_list = graph.get_adjacency_list()
    degrees = graph.get_out_degrees()

    curr_path = []
    cycle = []

    curr_path.append(start)
    curr_vertex = start
    while len(curr_path):
        if degrees[curr_vertex] != 0:
            curr_path.append(curr_vertex)
            next_vertex = adj_list[curr_vertex][-1]
            degrees[curr_vertex] -= 1
            adj_list[curr_vertex].pop()
            if not graph.directed:
                degrees[next_vertex] -= 1
                adj_list[next_vertex].remove(curr_vertex)
            curr_vertex = next_vertex
        else:
            cycle.append(curr_vertex)
            curr_vertex = curr_path[-1]
            curr_path.pop()

    return cycle[::-1]


def find_eulerian_cycle(graph, start=0):
    return hierholzer_cycle(graph, start)
