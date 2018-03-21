import os
import json
import xml.etree.ElementTree as ET

aids_data_folder = "data/AIDS/AIDS/data/"
protein_data_folder = "data/Protein/Protein/data/"
unwanted_files = ["test.cxl", "train.cxl", "valid.cxl"]

aids_json_folder = "data/aids_json/"
protein_json_folder = "data/protein_json/"


def main():
    aids_json = process_aids_data()
    # process_protein_data()


def process_aids_data():
    if not os.path.exists(aids_json_folder):
        os.mkdir(aids_json_folder)
    for f in os.listdir(aids_data_folder):
        if ".gxl" in f and f not in unwanted_files:
            fpath = aids_data_folder + f
            root = ET.parse(fpath).getroot()
            graph_node = root[0]
            g_id = graph_node.attrib['id']
            num_nodes = len([n for n in graph_node.iter('node')])
            node_list = [''] * num_nodes
            edge_list = [[0] * num_nodes for i in range(num_nodes)]
            for n in graph_node.iter('node'):
                n_id = int((n.attrib['id'])[1:]) - 1
                n_elem = (n[0][0].text).strip()
                node_list[n_id] = n_elem
            for e in graph_node.iter('edge'):
                e_from = int((e.attrib['from'])[1:]) - 1
                e_to = int((e.attrib['to'])[1:]) - 1
                e_bond = int((e[0][0].text).strip())
                edge_list[e_from][e_to] = e_bond
                edge_list[e_to][e_from] = e_bond
            g = {"n": node_list, "e": edge_list}
            graph_json_file = aids_json_folder + f[:-3] + "json"
            with open(graph_json_file, 'w') as outfile:
                print("Creating : " + graph_json_file)
                json.dump(g, outfile)


def process_protein_data():
    if not os.path.exists(protein_json_folder):
        os.mkdir(protein_json_folder)
    for f in os.listdir(protein_data_folder):
        if ".gxl" in f and f not in unwanted_files:
            fpath = protein_data_folder + f
            root = ET.parse(fpath).getroot()
            graph_node = root[0]


if __name__ == '__main__':
    main()
