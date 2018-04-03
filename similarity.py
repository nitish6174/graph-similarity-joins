import json
from algo_veo import vertex_edge_overlap
from algo_vs import vertex_edge_vector_similarity

# Constants
data_folder = "data/"

# Vertex counts for which graph data is generated
v_counts = [10, 100]

# Density modes for which graphs are generated
graph_densities = ["sparse", "normal", "dense"]

# Similarity threshold above which pairs are to be found
sim_threshold = 0.9


def main():
    print("Similarity threshold :", sim_threshold)
    # Load dataset for each combination of vertex count and graph density
    for v_count in v_counts:
        for d in graph_densities:
            print("\n\n" + "-" * 10)
            data1 = load_data(v_count, d, "A")
            data2 = load_data(v_count, d, "B")
            pairwise_similarity(data1, data2)


def pairwise_similarity(set1, set2):
    for i in range(len(set1)):
        for j in range(len(set2)):
            sim_veo = vertex_edge_overlap(set1[i], set2[j])
            sim_vs = vertex_edge_vector_similarity(set1[i], set2[j])
            s = "A" + str(i+1) + " and B" + str(j+1) + " :"
            if sim_veo > sim_threshold:
                print("\n" + s)
                print("  Vertex Edge Overlap : " + str(sim_veo))
                print("  Vector Similarity   : " + str(sim_vs))
                # print(set1[i]["e_list"])
                # print(set2[j]["e_list"])


def load_data(v_count, d, set_label):
    file = data_folder + str(v_count) + "_" + d + "_" + set_label + ".json"
    print("Loading : " + file, end=" . . . ")
    with open(file) as f:
        data = json.load(f)
    for x in data:
        generate_vertex_index_list(x, v_count)
    print("Done !")
    return data


def generate_vertex_index_list(g, v_count):
    l = [-1] * v_count
    index = 0
    for v in g["vertices"]:
        l[v] = index
        index += 1
    g["v_index"] = l


if __name__ == '__main__':
    main()
