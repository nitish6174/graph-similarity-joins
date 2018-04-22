import os
import json
import numpy as np
import matplotlib.pyplot as plt
from config import *

review_method = "veo"


def main():
    # Make analysis directory
    if not os.path.exists(analysis_folder):
        os.mkdir(analysis_folder)
    if not os.path.exists(param_analysis_plots_folder):
        os.mkdir(param_analysis_plots_folder)
    # Plot seperately for undirected & directed graph datasets
    for t in graph_types:
        print("-" * 10)
        print("type :", t)
        data = []
        # Generate plot for 2 types each of size, density, max edge weight
        for n in [v_counts[0], v_counts[-1]]:
            for d in [graph_densities[0], graph_densities[-1]]:
                for w in [max_edge_weights[0], max_edge_weights[-1]]:
                    res = load_sim_results(n, d, t, w)
                    a = get_sim_array(res)
                    data.append({
                        "v_count": n,
                        "density": d,
                        "max_weight": w,
                        "sim_val": a
                    })
        scatterplot(t, data)


def load_sim_results(n, d, t, w):
    f_title = str(n) + "_" + d + "_" + t + "_" + str(w)
    file_path = result_folder + f_title + ".json"
    print("Loading : " + file_path, end=" . . . ")
    with open(file_path) as f:
        data = json.load(f)
    print("Done !")
    return data


def get_sim_array(res):
    sim_val = []
    # Loop through each graph pair result
    # and get value corresponding to review_method
    for i in res:
        for j in res[i]:
            sim_val.append(res[i][j]["method"][review_method])
    return sim_val


def save_analysis(results):
    file = analysis_folder + "method_comparison.json"
    print("Saving : " + file, end=" . . . ")
    with open(file, 'w') as f:
        f.write(json.dumps(results))
    print("Done !\n")


def scatterplot(t, data):
    # Create label array and y data
    labels = []
    y = []
    for x in data:
        l = "n=" + str(x["v_count"]) + "\n" + \
            "d=" + str(x["density"]) + "\n" + \
            "w=" + str(x["max_weight"])
        labels.append(l)
        y.append(x["sim_val"])
    y = np.array(y)
    colors = ["crimson", "purple", "green", "gold"]
    width = 0.4
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, l in enumerate(labels):
        x = np.ones(y.shape[1])*i + (np.random.rand(y.shape[1])*width-width/2.)
        ax.scatter(x, y[i,:], color=colors[i%len(colors)], s=1)
        mean = y[i,:].mean()
        ax.plot([i-width/2., i+width/2.],[mean,mean], color="k")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    f_name = review_method + "_" + t + ".png"
    file_path = param_analysis_plots_folder + f_name
    plt.savefig(file_path, bbox_inches='tight')


if __name__ == '__main__':
    main()
