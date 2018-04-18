from vertex_quality import compute_vertex_quality


def sequence_similarity(g1, g2):
    # Compute quality of vertices
    vq1 = compute_vertex_quality(g1, "degree_normalised")
    vq2 = compute_vertex_quality(g2, "degree_normalised")
    # Get sequence representation of graph
    # seq1 = graph_to_node_sequence(g1, vq1)
    # seq2 = graph_to_node_sequence(g2, vq2)
    return 0.5


def graph_to_node_sequence(g, vq):
    # Find quality of all vertices
    vertex_degree = compute_vertex_quality(g, "degree_normalised")
    # Use double dictionary to store edge quality
    # Thus q(u,v) can be accessed by eq[u][v]
    eq = {}
    v_set = g["vertices"]
    n = len(v_set)
    for i in range(n):
        u = v_set[i]
        eq[u] = {}
        for j in range(i+1, n):
            eq[u][v_set[j]] = vq[u] * 1.0 / vertex_degree[u]
    return eq
