# Folders
data_folder = "data/"
result_folder = "results/"

# Graph parameters for which datset is generated
# Max vertex label in any graph of a set
v_counts = [10, 25, 50]
graph_densities = ["sparse", "normal", "dense"]
graph_types = ["undirected", "directed"]
max_edge_weights = [1, 5, 10]

# Min fraction of vertices to generate corresponding to each v_count
min_v_fraction = 0.7

# No of graphs to be generated for a chosen parameter combination
n_graphs = 100
