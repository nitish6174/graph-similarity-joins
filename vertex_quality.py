from math import sqrt
import numpy as np


def compute_vertex_quality(g, g_type, method="pagerank"):
    if method == "in_degree":
        return vertex_degree(g, g_type, "in")
    if method == "out_degree":
        return vertex_degree(g, g_type, "out")
    if method == "degree":
        return vertex_degree(g, g_type, "total")
    if method == "degree_normalised":
        return vertex_degree_normalised(g, g_type)
    if method == "pagerank":
        return pagerank(g, g_type)


def vertex_degree(g, g_type, degree_type="total"):
    # Initialize degree of all vertices as 0
    q = {}
    for v in g["vertices"]:
        q[v] = 0
    # Increment degree of edge endpoints accordingly
    for e in g["e_list"]:
        if g_type == "undirected" or degree_type == "total":
            q[e[0]] += e[2]
            q[e[1]] += e[2]
        elif degree_type == "out":
            q[e[0]] += e[2]
        elif degree_type == "in":
            q[e[1]] += e[2]
    return q


def vertex_degree_normalised(g, g_type, degree_type="total"):
    # Get degree of all vertices
    q = vertex_degree(g, g_type, degree_type)
    # Normalise the degree
    norm = sqrt(sum([ q[k]**2 for k in q]))
    for k in q:
        q[k] /= norm
    return q


def pagerank(g, g_type):
    n = len(g["vertices"])
    # Make transition weightage matrix
    P = np.zeros((n, n))
    for i in range(n):
        out_w = sum(g["e_matrix"][i])
        if out_w > 0:
            for j in range(n):
                P[j][i] = g["e_matrix"][i][j] / out_w
    # Initialize rank matrix
    r0 = np.full((n, 1), 1.0/n)
    # Keep on generating next iteration by multiplying P
    # Convergence occurs when values in consecutive iteration are close enough
    # Here we are comparing current rank vector with previous 4 iterations
    r1 = np.matmul(P, r0)
    r2 = np.matmul(P, r1)
    r3 = np.matmul(P, r2)
    r4 = np.matmul(P, r3)
    while not are_close(r0, r1, r2, r3, r4):
        r0 = np.matmul(P, r4)
        r1 = np.matmul(P, r0)
        r2 = np.matmul(P, r1)
        r3 = np.matmul(P, r2)
        r4 = np.matmul(P, r3)
    # Make quality dictionary
    q = {}
    for i in range(n):
        v = g["vertices"][i]
        q[v] = r4[i][0]
    return q


def are_close(r0, r1, r2, r3, r4):
    c0 = np.allclose(np.sort(r0, 0), np.sort(r4, 0))
    c1 = np.allclose(np.sort(r1, 0), np.sort(r4, 0))
    c2 = np.allclose(np.sort(r2, 0), np.sort(r4, 0))
    c3 = np.allclose(np.sort(r3, 0), np.sort(r4, 0))
    return (c0 or c1 or c2 or c3)
