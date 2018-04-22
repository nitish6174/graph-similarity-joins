import os
import json
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt
from config import *


def main():
    # Make analysis directory
    if not os.path.exists(analysis_folder):
        os.mkdir(analysis_folder)
    method_sim_values = []
    # Loop through parameters and load corresponding result file
    for n in v_counts:
        for d in graph_densities:
            for t in graph_types:
                for w in max_edge_weights:
                    print("-" * 10)
                    print("v_count    :", n)
                    print("density    :", d)
                    print("type       :", t)
                    print("max_weight :", w)
                    res = load_sim_results(n, d, t, w)
                    a = make_arrays(res)
                    method_sim = compute_method_similarity(a)
                    method_sim_values.append({
                        "v_count": n,
                        "density": d,
                        "g_type": t,
                        "max_weight": w,
                        "method_similarity": method_sim
                    })
                    scatterplot(n, d, t, w, a)
    # Save analysis results
    # save_analysis(method_sim_values)


def load_sim_results(n, d, t, w):
    f_title = str(n) + "_" + d + "_" + t + "_" + str(w)
    file_path = result_folder + f_title + ".json"
    print("Loading : " + file_path, end=" . . . ")
    with open(file_path) as f:
        data = json.load(f)
    print("Done !")
    return data


def make_arrays(d):
    # Extract method names stored in d
    # (keys are of type method and method_time)
    methods = [k for k in d["0"]["0"]["method"]]
    # Make a dictionary containing sim_val array for each method
    sim_val = {x:[] for x in methods}
    # Loop through each graph pair result and methods for that pair
    for i in d:
        for j in d[i]:
            for k in d[i][j]["method"]:
                sim_val[k].append(d[i][j]["method"][k])
    return sim_val


def compute_method_similarity(a):
    methods = [k for k in a]
    method_sim = []
    for i in range(len(methods)):
        for j in range(i+1, len(methods)):
            x, y = methods[i], methods[j]
            val = 1 - spatial.distance.cosine(a[x], a[y])
            method_sim.append((x, y, val))
            print("Method '" + x + "' vs '" + y + "' :", val)
    return method_sim


def save_analysis(results):
    file = analysis_folder + "method_comparison.json"
    print("Saving : " + file, end=" . . . ")
    with open(file, 'w') as f:
        f.write(json.dumps(results))
    print("Done !\n")


def scatterplot(n, d, t, w, a):
    labels = [k for k in a]
    colors = ["crimson", "purple", "green", "red", "blue"]
    data = np.array([a[x] for x in labels])
    width = 0.4
    fig, ax = plt.subplots()
    for i, l in enumerate(labels):
        x = np.ones(data.shape[1])*i + (np.random.rand(data.shape[1])*width-width/2.)
        ax.scatter(x, data[i,:], color=colors[i], s=1)
        mean = data[i,:].mean()
        ax.plot([i-width/2., i+width/2.],[mean,mean], color="k")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    f_title = str(n) + "_" + d + "_" + t + "_" + str(w)
    file_path = analysis_folder + "scatter_" + f_title + ".png"
    plt.savefig(file_path)


if __name__ == '__main__':
    main()
