import os
import math
import json
import random

# Constants
data_folder = "data/"

# Max vertex labels for which graph data is generated
v_counts = [10, 100]

# Min fraction of vertices to generate corresponding to each v_count
min_v_fraction = 0.7

# Density modes for which graphs are generated
graph_densities = ["sparse", "normal", "dense"]

# No of graphs to be generated for a chosen (v_count, graph_density)
n_graphs = 100


def main():
    # Make data directory
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    # Generate dataset for each combination of vertex count and graph density
    for v_count in v_counts:
        for d in graph_densities:
            make_random_graphs(v_count, d)


def make_random_graphs(v_count, d):
    print("Generating graph data for:")
    print("  v_count : " + str(v_count))
    print("  density : " + d)
    # Generate list of vertex labels
    v_labels = [x for x in range(v_count)]
    # Loop to generate graphs for set A and B
    for set_label in ("A", "B"):
        data = []
        for i in range(n_graphs):
            # Number of vertices to generate
            v_set_len = random.randint( int(min_v_fraction*v_count), v_count)
            # Generate random set of vertex labels of len v_set_len
            random.shuffle(v_labels)
            v_set = v_labels[:v_set_len]
            v_set.sort()
            # No. of edges to be kept in current graph
            n_edges = num_edges(v_set_len, d)
            # Generate edge matrix forming a connected graph
            e_matrix, e_list = make_connected_graph(v_count, v_set, n_edges)
            # Append label, vertex set, edges of this graph to set
            g = {
                "label": set_label + str(i+1),
                "vertices": v_set,
                "e_list": e_list,
                "e_matrix": e_matrix
            }
            data.append(g)
        # Store graph set data in JSON file
        file_name = str(v_count) + "_" + d + "_" + set_label + ".json"
        print("Generating " + file_name + " . . . ", end="")
        with open(data_folder + file_name, 'w') as f:
            f.write(json.dumps(data))
        print("Done!")
    print("")


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
        l_mark = int(a)
        u_mark = int(b)
    elif density == "dense":
        l_mark = int(c)
        u_mark = int(d)
    else:
        l_mark = int(b)
        u_mark = int(c)
    return random.randint(l_mark, u_mark)


def make_connected_graph(v_count, v_set, n_edges):
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
        v_to_add = random.sample(v_unadded, 1)[0]
        v_added.add(v_to_add)
        v_unadded.remove(v_to_add)
        v_to_connect = random.sample(v_added, 1)[0]
        u = node_to_e_matrix_index[v_to_add]
        v = node_to_e_matrix_index[v_to_connect]
        e_matrix[u][v], e_matrix[v][u] = 1, 1
        n_edges -= 1
    # Now, as graph is a single component hence add rest edges randomly
    e_unadded = []
    for i in range(v_set_len):
        for j in range(i+1, v_set_len):
            if e_matrix[i][j] == 0:
                e_unadded.append((i, j))
            else:
                e_list.append((i, j))
    random.shuffle(e_unadded)
    for i in range(n_edges):
        u, v = e_unadded[i][0], e_unadded[i][1]
        e_matrix[u][v], e_matrix[v][u] = 1, 1
        e_list.append((u, v))
    e_list.sort()
    return e_matrix, e_list


if __name__ == '__main__':
    main()
