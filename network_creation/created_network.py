import os
import json
from networkx.readwrite import json_graph
from definitions import ROOT_DIR

folder = ROOT_DIR + "/graph_data/"

def save_graph(graph, filename):
    graph_json = json_graph.node_link_data(graph)
    with open(os.path.join(folder + filename + "_graph.json"), "w") as f:
        json.dump(graph_json, f)


def get_graph(filename):
    with open(os.path.join(folder + filename + "_graph.json"), "r") as f:
        graph_json = json.load(f)
    return json_graph.node_link_graph(graph_json)
