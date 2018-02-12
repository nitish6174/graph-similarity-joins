import json
import random

# Constants
data_folder = "data/"

# Vertex counts for which graph data is generated
v_counts = [10, 50, 100]

# Fraction of vertices out of each v_num entry
# which should be present in each graph
v_fraction = 0.9

# Density modes for which graphs are generated
graph_densities = ["sparse", "normal", "dense"]


def main():
    # Generate dataset for each combination of vertex count and graph density
    for v_count in v_counts:
        for d in graph_densities:
            make_random_graphs(v_count, d)


def make_random_graphs(v_count, d):
    # Vertex labels
    v_labels = [x for x in range(v_count)]
    v_set_len = int(v_count * v_fraction)
    # No. of edges (as range) to be kept in a generated graph
    n_edges = num_edges_range(v_count, d)
    # No. of graphs to be generated in each set
    n_graphs = set_cardinality(n_edges[0])
    print("Generating graph data for:")
    print("v_count  : " + str(v_count))
    print("density  : " + d)
    print("n_graphs : " + str(n_graphs))
    # Loop to generate graphs for set A and B
    for set_label in ("A", "B"):
        data = []
        for i in range(n_graphs):
            # Generate random set of vertex labels of len v_set_len
            random.shuffle(v_labels)
            v_set = v_labels[:v_set_len]
            v_set.sort()
            # No. of edges in graph is randomly selected from
            # the range returned by num_edges_range()
            e_set_len = random.randint(n_edges[1], n_edges[2])
            # Generate list of all possible edges
            # and randomly choose required no. from them
            e_list = [
                (v_set[i], v_set[j])
                for i in range(v_set_len)
                for j in range(i+1, v_set_len)
            ]
            random.shuffle(e_list)
            e_list = e_list[:e_set_len]
            # Append label, vertex set, edge set of this graph to set
            g = {
                "label": set_label + str(i+1),
                "vertices": v_set,
                "edges": e_list
            }
            data.append(g)
        # Store graph set data in JSON file
        file_name = str(v_count) + "_" + d + "_" + set_label + ".json"
        print("Generating " + file_name + " . . . ", end="")
        with open(data_folder + file_name, 'w') as f:
            f.write(json.dumps(data))
        print("Done!")
    print("")


def num_edges_range(num_v, density="normal"):
    """
    Returns no. of edges that must be generated in graph
    depending on density given
        sparse : no. of edges lies around (v-1)^1.0 * 2
        normal : no. of edges lies around (v-1)^1.5
        dense  : no. of edges lies around (v-1)^2.0 / 2
    """
    if density == "sparse":
        mark = (num_v-1) * 2
        l_mark = max(int(0.9*mark), num_v+1)
        u_mark = int(1.1*mark)
    elif density == "dense":
        mark = ((num_v-1)**2) * 0.5
        l_mark = int(0.9*mark)
        u_mark = min( int(1.1*mark), (num_v*(num_v-1)/2)-1 )
    else:
        mark = (num_v-1)**1.5
        l_mark = int(0.9*mark)
        u_mark = int(1.1*mark)
    return (int(mark), l_mark, u_mark)


def set_cardinality(num_edges):
    """
    No. of graph generated in either set_cardinality corresponding to
    a particular combination of v_num and density
    """
    return num_edges


if __name__ == '__main__':
    main()
