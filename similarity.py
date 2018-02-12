import json
from algo_veo import vertex_edge_overlap

# Constants
data_folder = "data/"

# Vertex counts for which graph data is generated
v_counts = [10, 50, 100]
v_counts = [10]

# Density modes for which graphs are generated
graph_densities = ["sparse", "normal", "dense"]
graph_densities = ["sparse"]


def main():
    # Load dataset for each combination of vertex count and graph density
    for v_count in v_counts:
        for d in graph_densities:
            data1 = load_data(v_count, d, "A")
            data2 = load_data(v_count, d, "B")
            pairwise_similarity(data1, data2)


def pairwise_similarity(set1, set2):
    for i in range(len(set1)):
        for j in range(len(set2)):
            sim_veo = vertex_edge_overlap(set1[i], set2[j])
            s = "Similarity between A" + str(i+1) + " and B" + str(j+1) + " :"
            print("\n" + s)
            print("  Vertex Edge Overlap : " + str(sim_veo))


def load_data(v_count, d, set_label):
    file = data_folder + str(v_count) + "_" + d + "_" + set_label + ".json"
    print("Loading : " + file, end=" . . . ")
    with open(file) as f:
        data = json.load(f)
    for x in data:
        generate_edge_matrix(x, v_count)
    print("Done !")
    return data


def generate_edge_matrix(g, v_count):
    generate_vertex_index_list(g, v_count)
    n = len(g["vertices"])
    e_matrix = [[0]*n for _ in range(n)]
    for e in g["edges"]:
        v1 = g["v_index"][e[0]]
        v2 = g["v_index"][e[1]]
        e_matrix[v1][v2] = 1
        e_matrix[v2][v1] = 1
    g["e_matrix"] = e_matrix


def generate_vertex_index_list(g, v_count):
    l = [-1] * v_count
    index = 0
    for v in g["vertices"]:
        l[v] = index
        index += 1
    g["v_index"] = l


if __name__ == '__main__':
    main()
