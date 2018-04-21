import os
import math
import json
import random
import time
from config import *
from algo.vertex_quality import compute_vertex_quality


def main():
    # Make data directory
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    # Generate dataset for each combination of vertex count and graph density
    for n in v_counts:
        for d in graph_densities:
            for t in graph_types:
                for w in max_edge_weights:
                    start = time.time()
                    make_random_graphs(n, d, t, w)
                    end = time.time()
                    print("Time taken :", end - start)
                    print("-" * 10, "\n")


def make_random_graphs(v_count, d_type, g_type, m_weight):
    f_title = str(v_count) + "_" + d_type + "_" + g_type + "_" + str(m_weight)
    print("Generating graph data for:")
    print("  v_count          :", v_count)
    print("  density          :", d_type)
    print("  graph type       :", g_type)
    print("  max edge weight  :", m_weight)
    # Generate list of vertex labels
    v_labels = [x for x in range(v_count)]
    # Loop to generate graphs for set A and B
    for set_label in ("A", "B"):
        data = []
        for i in range(n_graphs):
            # Number of vertices to generate
            v_set_len = random.randint(int(min_v_fraction*v_count), v_count)
            # Generate random set of vertex labels of size v_set_len
            random.shuffle(v_labels)
            v_set = v_labels[:v_set_len]
            v_set.sort()
            # No. of edges to be kept in current graph
            n_edges = num_edges(v_set_len, d_type)
            if g_type == "directed":
                n_edges *= 2
            # Generate edge matrix forming a connected graph
            e_matrix, e_list = make_connected_graph(
                v_count, v_set, n_edges, g_type, m_weight
            )
            # Append label, vertex set, edges of this graph to set
            g = {
                "label": set_label + str(i+1),
                "vertices": v_set,
                "e_list": e_list,
                "e_matrix": e_matrix
            }
            q = compute_vertex_quality(g, g_type)
            g["v_quality"] = q
            data.append(g)
        # Store graph set data in JSON file
        file_path = data_folder + f_title + "_" + set_label + ".json"
        print("Generating " + file_path + " . . . ", end="")
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))
        print("Done!")


def num_edges(num_v, density="normal"):
    """
    Returns no. of edges that must be generated in graph
    depending on density given
        Take a = v
             d = v * (v-1) / 2
             and the interval [ sqrt(a), sqrt(d) ] is uniformly divided by
             sqrt(b) and sqrt(c)
             i.e. sqrt(b) - sqrt(a) = sqrt(c) - sqrt(b) = sqrt(d) - sqrt(c)
        sparse : num_nodes between a to b
        normal : num_nodes between b to c
        dense  : num_nodes between c to d
    """
    a = num_v
    d = a * (a-1) / 2
    b = ((2*math.sqrt(a) + math.sqrt(d))/3)**2
    c = ((math.sqrt(a) + 2*math.sqrt(d))/3)**2
    if density == "sparse":
        l_mark, u_mark = a, b
    elif density == "dense":
        l_mark, u_mark = c, d
    else:
        l_mark, u_mark = b, c
    return random.randint(int(l_mark), int(u_mark))


def make_connected_graph(v_count, v_set, n_edges, g_type, m_weight):
    # Use 2 sets of vertices to get all vertices connected in same component
    v_added = set([])
    v_unadded = set([v for v in v_set])
    # Initialize edge list and matrix with no edge
    v_set_len = len(v_set)
    e_list = []
    e_matrix = [[0]*v_set_len for _ in range(v_set_len)]
    # Make a mapping from node label to its corresponding index in edge matrix
    node_to_e_matrix_index = {}
    matrix_index = 0
    for x in v_set:
        node_to_e_matrix_index[x] = matrix_index
        matrix_index += 1
    # Add a random non-added vertex to graph
    v_to_add = random.sample(v_unadded, 1)[0]
    v_added.add(v_to_add)
    v_unadded.remove(v_to_add)
    # Repeatedly connect a non-added vertex to any of the added ones
    while len(v_unadded) > 0:
        v_to_connect = random.sample(v_added, 1)[0]
        v_to_add = random.sample(v_unadded, 1)[0]
        v_added.add(v_to_add)
        v_unadded.remove(v_to_add)
        u = node_to_e_matrix_index[v_to_add]
        v = node_to_e_matrix_index[v_to_connect]
        e_weight = random.randint(1, m_weight)
        e_matrix[u][v] = e_weight
        if g_type == "undirected":
            e_matrix[v][u] = e_weight
        n_edges -= 1
    # Now, as graph is a single component hence add rest edges randomly
    e_unadded = []
    for i in range(v_set_len):
        if g_type == "directed":
            j_start = 0
        else:
            j_start = i + 1
        for j in range(j_start, v_set_len):
            if i != j:
                if e_matrix[i][j] == 0:
                    e_weight = random.randint(1, m_weight)
                    e_unadded.append((i, j, e_weight))
                else:
                    e_list.append((v_set[i], v_set[j], e_matrix[i][j]))
    random.shuffle(e_unadded)
    for i in range(n_edges):
        u, v, w = e_unadded[i][0], e_unadded[i][1], e_unadded[i][2]
        e_matrix[u][v] = w
        if g_type == "undirected":
            e_matrix[v][u] = w
        e_list.append((v_set[u], v_set[v], w))
    e_list.sort()
    return e_matrix, e_list


if __name__ == '__main__':
    main()
