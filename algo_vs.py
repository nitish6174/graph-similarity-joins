from vertex_quality import compute_vertex_quality


def vertex_edge_vector_similarity(g1, g2, g_type):
    # Compute out-degree and quality of vertices
    od1 = compute_vertex_quality(g1, g_type, "out_degree")
    od2 = compute_vertex_quality(g2, g_type, "out_degree")
    # Compute edge weightage
    eq1 = compute_edge_weightage(g1, od1)
    eq2 = compute_edge_weightage(g2, od2)
    # Loop through all edges of g1, compare its weightage
    # with corresponding edge in g2 and add penalty
    penalty = 0.0
    num_edges_union = 0
    for u in eq1:
        for v in eq1[u]:
            num_edges_union += 1
            if u in eq2 and v in eq2[u]:
                w1, w2 = eq1[u][v], eq2[u][v]
                penalty += abs(w1 - w2) / max(w1, w2)
            else:
                penalty += 1
    # Now add penalty score for edges in g2 but not in g1
    for u in eq2:
        for v in eq2[u]:
            if u not in eq1 or v not in eq1[u]:
                num_edges_union += 1
                penalty += 1
    # Similarity is given by 1 - (penalty / no. of edges in union of graphs)
    sim_val = 1.0 - penalty / num_edges_union
    return sim_val


def compute_edge_weightage(g, out_degree):
    # Use double dictionary to store edge quality
    # Thus q(u,v) can be accessed by eq[u][v]
    eq = {}
    v_set = g["vertices"]
    n = len(v_set)
    for i in range(n):
        u = v_set[i]
        q_u = g["v_quality"][str(u)]
        eq[u] = {}
        for j in range(n):
            w = g["e_matrix"][i][j]
            if w != 0:
                v = v_set[j]
                eq[u][v] = q_u * w / out_degree[u]
    return eq
