from math import sqrt


def compute_vertex_quality(g, method="degree_normalised"):
    if method == "degree":
        return vertex_degree(g)
    if method == "degree_normalised":
        return vertex_degree_normalised(g)


def vertex_degree(g):
    # Initialize degree of all vertices as 0
    d = {}
    for v in g["vertices"]:
        d[v] = 0
    # For both endpoint of each edge, increment their quality
    for e in g["e_list"]:
        d[e[0]] += 1
        d[e[1]] += 1
    return d


def vertex_degree_normalised(g):
    # Get degree of all vertices
    q = vertex_degree(g)
    # Normalise the degree
    norm = sqrt(sum([ q[k]**2 for k in q]))
    for k in q:
        q[k] /= norm
    return q
