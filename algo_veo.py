def vertex_edge_overlap(g1, g2):
    num1 = vertex_intersection_len(g1, g2)
    num2 = edge_intersection_len(g1, g2)
    den1 = len(g1["vertices"]) + len(g2["vertices"])
    den2 = len(g1["edges"]) + len(g2["edges"])
    return 2.0 * (num1+num2) / (den1+den2)


def vertex_intersection_len(g1, g2):
    v_i = set(g1["vertices"]) & set(g2["vertices"])
    return len(v_i)


def edge_intersection_len(g1, g2):
    if len(g1["edges"]) < len(g2["edges"]):
        e_list = g1["edges"]
        e_matrix = g2["e_matrix"]
        v_index = g2["v_index"]
    else:
        e_list = g2["edges"]
        e_matrix = g1["e_matrix"]
        v_index = g1["v_index"]
    count = 0
    for e in e_list:
        v1 = v_index[e[0]]
        v2 = v_index[e[1]]
        count += e_matrix[v1][v2]
    return count