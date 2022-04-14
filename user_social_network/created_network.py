import json
from networkx.readwrite import json_graph

def save_graph(graph):
    graph_json = json_graph.node_link_data(graph)
    json.dump(graph_json, open('graph.json','w'))

def get_graph():
    with open('graph.json') as f:
        graph_json = json.load(f)
    return json_graph.node_link_graph(graph_json)
