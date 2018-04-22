import os
import json
from config import *
from algo.algo_seqs import *

# Similarity thresholds above which pairs are to be found
sim_thresholds = [0.5, 0.7, 0.9]

# Verbose parameter for showing results while execution
verbose = 0


def main():
    # Make new dataset with node sequence
    pre_process()


def pre_process():
    if not os.path.exists(seq_data_folder):
        os.mkdir(seq_data_folder)
    # Iterate through all files in data folder
    for f_name in os.listdir(data_folder):
        data = load_data(f_name)
        # Loop through all graphs in loaded file
        # and find node sequence for the graphs
        for x in data:
            x["node_seq"] = graph_to_node_sequence(x)
        # Save the file with node_seq data
        save_results(data, f_name)


def load_data(f_name):
    print("Loading : " + f_name, end=" . . . ")
    with open(data_folder + f_name) as f:
        data = json.load(f)
    n = int((f_name.split("_"))[0])
    for x in data:
        generate_vertex_index_list(x, n)
    print("Done !")
    return data


def generate_vertex_index_list(g, v_count):
    """Array which maps vertex label to matrix index"""
    l = [-1] * v_count
    index = 0
    for v in g["vertices"]:
        l[v] = index
        index += 1
    g["v_index"] = l


def save_results(data, f_name):
    f_path = seq_data_folder + f_name
    print("Saving : " + f_path, end=" . . . ")
    with open(f_path, 'w') as f:
        f.write(json.dumps(data))
    print("Done !\n")


if __name__ == '__main__':
    main()
