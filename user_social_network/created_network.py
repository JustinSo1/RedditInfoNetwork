import os
import json
from networkx.readwrite import json_graph

def save_graph(graph):
    graph_json = json_graph.node_link_data(graph)
    with open(os.path.join("user_social_network", "graph.json"), "w") as f:
        json.dump(graph_json, f)

def get_graph():
    with open(os.path.join("user_social_network", "graph.json"), "r") as f:
        graph_json = json.load(f)
    return json_graph.node_link_graph(graph_json)
