from ctypes import Union

from sympy import N, erfinv
from created_network import get_graph
import networkx as nx
import pandas as pd

def get_top_n_degree_centrality(G, n):
    degree_centralities = nx.degree_centrality(G)
    degree_centralities = {node: centrality for node, centrality in sorted(degree_centralities.items(), key=lambda item: item[1], reverse=True)[:n]}

    return degree_centralities

# Only keep the users from network that are in bipartite
def filter_users(network, bipartite):
    network_nodes = network.nodes()
    bipartite_graph_nodes = bipartite.nodes()

    # TODO: Only 1k nodes are getting removed right now
    # Double check nodes and create graph scripts
    nodes_to_remove = list(set(network_nodes) - set(bipartite_graph_nodes))
    network.remove_nodes_from(nodes_to_remove)

    return network

def get_common_topics(degree_centralities, network, bipartite):
    # Return a df showing authors that share a common topic and their sentiments
    # {author1, author2, common_topic, sentiment1, sentiment2}

    # look through each node in the degree centrality
    # for each node, get their topics and sentiments
    # also get their neighbouring nodes
    # for each neighbouring nodes, get their topics and sentiments
    # compare with the node and their topics and sentiments
    # get intersection between 2 lists
    return 0

if __name__ == "__main__":
    user_social_network = get_graph("user_social_network")
    user_to_topic = get_graph("user_to_topic")
    # print(user_social_network.number_of_nodes())
    # print(user_to_topic.number_of_nodes())

    filtered_network_graph = filter_users(user_social_network, user_to_topic)
    # print(filtered_network_graph.number_of_nodes())

    degree_centralities = get_top_n_degree_centrality(filtered_network_graph, 1000)
