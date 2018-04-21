from operator import itemgetter
from config import *
from vertex_quality import compute_vertex_quality


def sequence_similarity(g1, g2, g_type):
    # Get sequence representation of graph
    seq1 = graph_to_node_sequence(g1)
    seq2 = graph_to_node_sequence(g2)
    # Create shingles for both sequence using size 3 node tokens
    sgl1, sgl2 = set(), set()
    n1, n2 = len(g1["vertices"]), len(g2["vertices"])
    for i in range(n1 - 2):
        val = seq1[i] * (sgl_val**2) + seq1[i+1] * sgl_val + seq1[i+2]
        sgl1.add(val)
    for i in range(n2 - 2):
        val = seq2[i] * (sgl_val**2) + seq2[i+1] * sgl_val + seq2[i+2]
        sgl2.add(val)
    num = len(sgl1 & sgl2)
    den = len(sgl1 | sgl2)
    return 1.0 * num / den


def graph_to_node_sequence(g):
    n = len(g["vertices"])
    # Maintain a quality dictionary
    q = {k:g["v_quality"][k] for k in g["v_quality"]}
    # Maintain an array containing (vertex_label, quality) tuples
    # in sorted order of quality
    v_quality_sorted = sorted([(k, q[k]) for k in q],
                              key=itemgetter(1), reverse=True)
    # Generate node sequence
    node_seq = []
    while len(node_seq) < n:
        # Find the highest quality unadded vertex
        # (added vertex will be marked with negative quality)
        pos = 0
        while q[v_quality_sorted[pos][0]] < 0:
            pos += 1
        # Add this vertex to sequence and mark its quality as negative
        v = int(v_quality_sorted[pos][0])
        node_seq.append(v)
        q[str(v)] = -1
        # Recursively visit & add highest quality neighbour of current vertex
        recurse_add_neighbour(g, node_seq, q, v)
    return node_seq


def recurse_add_neighbour(g, node_seq, q, v):
    n = len(g["vertices"])
    # Find matrix row no. of v
    row = g["v_index"][v]
    # Initialize neighbour with max quality as -1
    max_q_nb = -1
    # Loop through nodes to which outgoing edge is present
    for col in range(n):
        if g["e_matrix"][row][col] > 0:
            # If the quality of this neighbour is highest till now, update
            v_nb = g["vertices"][col]
            if (max_q_nb < 0) or (q[str(v_nb)] > q[str(max_q_nb)]):
                max_q_nb = v_nb
    # Check if the max_q_nb so found was unadded
    if (max_q_nb > 0) and (q[str(max_q_nb)] > 0):
        # Add this neighbour and recurse
        node_seq.append(max_q_nb)
        q[str(max_q_nb)] = -1
        recurse_add_neighbour(g, node_seq, q, max_q_nb)
