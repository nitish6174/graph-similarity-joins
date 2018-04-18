import os
import json
from config import *
from algo_veo import vertex_edge_overlap
from algo_vs import vertex_edge_vector_similarity
from algo_seqs import sequence_similarity

# Similarity threshold above which pairs are to be found
sim_threshold = 0.9

# Verbose parameter for showing similarity score while execution
verbose = 0


def main():
    # Make result directory
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    if verbose:
        print("Similarity threshold :", sim_threshold)
    # Load dataset for each combination of parameters
    for n in v_counts:
        for d in graph_densities:
            for t in graph_types:
                for w in max_edge_weights:
                    print("\n" + "-" * 10)
                    print("v_count    :", n)
                    print("density    :", d)
                    print("type       :", t)
                    print("max_weight :", w)
                    data1 = load_data(n, d, t, w, "A")
                    data2 = load_data(n, d, t, w, "B")
                    print("Data loaded")
                    r = pairwise_similarity(data1, data2, t)
                    save_results(r, n, d, t, w)


def pairwise_similarity(set1, set2, g_type):
    result = {}
    for i in range(len(set1)):
        result[i] = {}
        for j in range(len(set2)):
            sim_veo = vertex_edge_overlap(set1[i], set2[j], g_type)
            # sim_vs = vertex_edge_vector_similarity(set1[i], set2[j], g_type)
            # sim_seqs = sequence_similarity(set1[i], set2[j], g_type)
            result[i][j] = {
                "veo" : sim_veo,
                # "vs" : sim_vs,
                # "seqs" : sim_seqs
            }
            s = "A" + str(i+1) + " and B" + str(j+1) + " :"
            if verbose and sim_veo > sim_threshold:
                print("\n" + s)
                print("  Vertex Edge Overlap : " + str(sim_veo))
                print("  Vector Similarity   : " + str(sim_vs))
                print("  Sequence Similarity   : " + str(sim_seqs))
                # print(set1[i]["e_list"])
                # print(set2[j]["e_list"])
    return result


def load_data(n, d, t, w, set_label):
    f_title = str(n) + "_" + d + "_" + t + "_" + str(w)
    file = data_folder + f_title + "_" + set_label + ".json"
    print("Loading : " + file, end=" . . . ")
    with open(file) as f:
        data = json.load(f)
    for x in data:
        generate_vertex_index_list(x, n)
    print("Done !")
    return data


def save_results(results, n, d, t, w):
    f_title = str(n) + "_" + d + "_" + t + "_" + str(w)
    file = result_folder + f_title + ".json"
    print("Saving : " + file, end=" . . . ")
    with open(file, 'w') as f:
        f.write(json.dumps(results))
    print("Done !\n")


def generate_vertex_index_list(g, v_count):
    l = [-1] * v_count
    index = 0
    for v in g["vertices"]:
        l[v] = index
        index += 1
    g["v_index"] = l


if __name__ == '__main__':
    main()
