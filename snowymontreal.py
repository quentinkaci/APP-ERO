import drone


def solve(is_oriented, num_vertices, edge_list):
    if is_oriented:
        return []  # FIXME
    else:
        return drone.solve(num_vertices, edge_list)
