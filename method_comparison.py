import os
import json
from scipy import spatial

# Constants
result_folder = "results/"

# Vertex counts for which graph data is generated
v_counts = [10, 100]

# Density modes for which graphs are generated
graph_densities = ["sparse", "normal", "dense"]


def main():
    for v_count in v_counts:
        for d in graph_densities:
            print("\n" + "-" * 10)
            # print("v_count :", v_count)
            # print("density :", d)
            d = load_sim_results(v_count, d)
            a = make_arrays(d)
            compute_method_similarity(a)


def load_sim_results(v_count, d):
    file = result_folder + str(v_count) + "_" + d + ".json"
    print("Loading : " + file, end=" . . . ")
    with open(file) as f:
        data = json.load(f)
    print("Done !\n")
    return data


def make_arrays(d):
    methods = [k for k in d["0"]["0"]]
    a = {}
    for x in methods:
        a[x] = []
    for i in d:
        for j in d[i]:
            for k in d[i][j]:
                a[k].append(d[i][j][k])
    return a


def compute_method_similarity(a):
    methods = [k for k in a]
    for i in range(len(methods)):
        for j in range(i+1, len(methods)):
            x, y = methods[i], methods[j]
            val = 1 - spatial.distance.cosine(a[x], a[y])
            print("Method '" + x + "' vs '" + y + "' :", val)


if __name__ == '__main__':
    main()
