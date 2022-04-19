import os

import networkx as nx
import pandas as pd

from created_network import get_graph
from definitions import ROOT_DIR
from sentiment_analysis import get_polarity


def get_top_n_degree_centralities(G, n):
    degree_centralities = nx.degree_centrality(G)
    degree_centralities = {node: centrality for node, centrality in
                           sorted(degree_centralities.items(), key=lambda item: item[1], reverse=True)[:n]}

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


# Return a df showing authors that share a common topic and their sentiments
# {author1, author2, common_topic, sentiment1, sentiment2}
def get_common_topics(degree_centralities, user_social_network, user_to_topic):
    # 1. Look through each node in degree_centralities
    # 2. For each node, get their topics // get user's neighbours (topic nodes) in user_to_topics
    # 3. Also get their neighbouring users from user_social_network // user_social_network.neighbours(user)
    # 4. Iterate through neighbours // does the neighbour exist in the topic's neighbour nodes (in user_to_topic)? Iterate thru all topics
    # 5. If yes, put the user and neighbour into the df with the sentiments towards the topic (from user_to_topic)

    author_common_topic_pairs = []

    for author in degree_centralities:
        author_topics = list(user_to_topic.neighbors(author))
        author_neighbours = list(user_social_network.neighbors(author))
        for topic in author_topics:
            topic_participants = list(user_to_topic.neighbors(topic))
            for neighbour in author_neighbours:
                if neighbour in topic_participants:
                    author_sentiment = get_polarity(user_to_topic.get_edge_data(author, topic)['avg_score'])
                    neighbour_sentiment = get_polarity(user_to_topic.get_edge_data(neighbour, topic)['avg_score'])
                    author_common_topic_pairs.append([author, neighbour, topic, author_sentiment, neighbour_sentiment])

    author_common_topic_pairs_df = pd.DataFrame(author_common_topic_pairs,
                                                columns=["author1", "author2", "common_topic", "sentiment1",
                                                         "sentiment2"])

    return author_common_topic_pairs_df


if __name__ == "__main__":
    user_social_network = get_graph(os.path.join(ROOT_DIR, "graph_data", "user_social_network"))
    user_to_topic = get_graph(os.path.join(ROOT_DIR, "graph_data", "user_to_topic"))

    filtered_network_graph = filter_users(user_social_network, user_to_topic)
    print(len(filtered_network_graph))  # 23163
    degree_centralities = get_top_n_degree_centralities(filtered_network_graph, len(filtered_network_graph))

    common_topics = get_common_topics(degree_centralities, user_social_network, user_to_topic)
    common_topics.to_csv(os.path.join(ROOT_DIR, "csv_data", "author_common_topic_pairs.csv"), index=False)
    print(len(common_topics))  # 35495
