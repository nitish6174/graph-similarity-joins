import os
import json
import random

# Constants
data_folder = "data/"

# Max vertex labels for which graph data is generated
v_counts = [10, 100, 1000]
v_counts = [10]

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
            # Fraction of vertices to generate
            v_fraction = random.uniform(min_v_fraction, 1.0)
            v_set_len = int(v_count * v_fraction)
            # Generate random set of vertex labels of len v_set_len
            random.shuffle(v_labels)
            v_set = v_labels[:v_set_len]
            v_set.sort()
            # No. of edges to be kept in current graph
            n_edges = num_edges(v_count, d)
            # Generate edge matrix forming a connected graph
            e_matrix = make_connected_graph(v_count, v_set, n_edges)
            # Append label, vertex set, edge set of this graph to set
            g = {
                "label": set_label + str(i+1),
                "vertices": v_set,
                "edges": e_matrix
            }
            data.append(g)
        # Store graph set data in JSON file
        file_name = str(v_count) + "_" + d + "_" + set_label + ".json"
        print("Generating " + file_name + " . . . ", end="")
        with open(data_folder + file_name, 'w') as f:
            f.write(json.dumps(data, indent=1))
        print("Done!")
    print("")


def num_edges(num_v, density="normal"):
    """
    Returns no. of edges that must be generated in graph
    depending on density given
        sparse : between v^1.0 to v^1.4 
        normal : between v^1.4 to v^1.7
        dense  : between v^1.7 to (v-1)^2 / 2
    """
    if density == "sparse":
        l_mark = num_v
        u_mark = int(num_v**1.4)
    elif density == "dense":
        l_mark = int( (num_v-1)**1.6)
        u_mark = int( (num_v-1)**2 / 2 )
    else:
        l_mark = int(num_v**1.4)
        u_mark = int(num_v**1.6)
    return random.randint(l_mark, u_mark)


def make_connected_graph(v_count, v_set, n_edges):
    # Use 2 sets of vertices to get all vertices connected in same component
    v_added = set([])
    v_unadded = set([v for v in v_set])
    # Initialize edge matric with no edge
    v_set_len = len(v_set)
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
    while len(v_unadded) > 1:
        v_to_add = random.sample(v_unadded, 1)[0]
        v_added.add(v_to_add)
        v_unadded.remove(v_to_add)
        v_to_connect = random.sample(v_added, 1)[0]
        u = node_to_e_matrix_index[v_to_add]
        v = node_to_e_matrix_index[v_to_connect]
        e_matrix[u][v], e_matrix[v][u] = 1, 1
        n_edges -= 1
    # Now, as graph is a single component hence add rest edges randomly
    # while n_edges > 0:
    #     u, v = random.randint(0, v_set_len-1), random.randint(0, v_set_len-1)
    #     if u != v and e_matrix[u][v] == 0:
    #         e_matrix[u][v], e_matrix[v][u] = 1, 1
    #         n_edges -= 1
    return e_matrix


if __name__ == '__main__':
    main()
