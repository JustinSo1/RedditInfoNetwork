import networkx as nx


def create_bipartite_graph(df):
    graph = nx.Graph()
    authors = df['author'].tolist()
    graph.add_nodes_from(authors, bipartite=0)
    topics = df['topic'].tolist()
    graph.add_nodes_from(topics, bipartite=1)
    for index, row in df.iterrows():
        author = row['author']
        topic = int(row['topic'])
        avg_score = float(row['avg_score'])
        graph.add_edge(author, topic, avg_score=avg_score)
    return graph, authors, topics
