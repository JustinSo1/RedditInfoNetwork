import csv
import matplotlib.pyplot as plt
import networkx as nx
from user_social_network.created_network import get_graph

def get_network_analysis(graph):
    # of nodes, # of edges and # of interactions for graph
    num_nodes, num_edges, num_interactions = get_num_nodes_edges_interactions(graph)

    # Node degree distribution scatter plot
    get_node_degree_distribution(graph)
    # Clustering coefficient scatter plot and get average clustering coefficient
    avg_cc = get_clustering_coefficient(graph)

    # Weakly connected component scatter plot and get largest weakly connected component
    wcc_graph = get_weakly_connected_component(graph)
    # of nodes, # of edges and # of interactions for wcc_graph
    num_nodes_wcc, num_edges_wcc, num_interactions = get_num_nodes_edges_interactions(wcc_graph)

    # Shortest path lengths scatter plot
    plot_shortest_path_length(graph)

    avg_shortest_path_wcc = get_avg_shortest_path_length(wcc_graph)
    # Get largest strongly connected component
    scc_graph = get_strongly_connected_component(graph)
    # of nodes, # of edges and # of interactions for scc_graph
    num_nodes_scc, num_edges_scc, num_interactions = get_num_nodes_edges_interactions(scc_graph)
    # Diameter
    dia = get_diameter(scc_graph)

    with open('network_analysis.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        component_type = ['All Components', 'Weakly Connected Component', 'Strongly Connected Component']

        ac_header = ['Num of Nodes', 'Num of Edges', 'Num of Interactions', 'Global Clustering Coefficient']
        ac_data = [num_nodes, num_edges, num_interactions, avg_cc]
        writer.writerow([component_type[0]])
        writer.writerow(ac_header)
        writer.writerow(ac_data)

        wcc_header = ['Num of Nodes', 'Num of Edges', 'Num of Interactions', 'Average Shortest Path']
        wcc_data = num_nodes_wcc, num_edges_wcc, num_interactions, avg_shortest_path_wcc
        writer.writerow([component_type[1]])
        writer.writerow(wcc_header)
        writer.writerow(wcc_data)

        scc_header = ['Num of Nodes', 'Num of Edges', 'Num of Interactions', 'Diameter']
        scc_data = num_nodes_scc, num_edges_scc, num_interactions, dia
        writer.writerow([component_type[2]])
        writer.writerow(scc_header)
        writer.writerow(scc_data)


def create_graph_analysis(x, y, title, xlabel, ylabel, file_name):
    # create scatter plots
    plt.scatter(x, y)
    plt.loglog(base=10)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(file_name)
    plt.clf()


def get_num_nodes_edges_interactions(graph):
    return graph.number_of_nodes(), graph.number_of_edges(), graph.size(weight='weight')


def get_x_axis_values(values):
    x_axis_values = list(set(values))  # remove duplicates
    return x_axis_values


def get_y_axis_values(values):
    # count frequency and calculate log for y-axis
    y_axis_values = [values.count(v) for v in get_x_axis_values(values)]
    return y_axis_values


def get_node_degree_distribution(graph):
    # the degree is the sum of the edge weights adjacent to the node.
    # all degrees
    d = [k for n, k in graph.degree(weight='weight')]
    create_graph_analysis(get_x_axis_values(d), get_y_axis_values(d), "Degree Distribution", "Degree, k", "Count, Nk",
                          "graphs/dd_all.png")

    # in-degrees
    ind = [k for n, k in graph.in_degree(weight='weight')]
    create_graph_analysis(get_x_axis_values(ind), get_y_axis_values(ind), "In Degree Distribution", "In Degree, k",
                          "Count, Nk", "graphs/dd_in.png")

    # out-degrees
    outd = [k for n, k in graph.out_degree(weight='weight')]
    create_graph_analysis(get_x_axis_values(outd), get_y_axis_values(outd), "Out Degree Distribution", "Out Degree, k",
                          "Count, Nk", "graphs/dd_out.png")

    plt.scatter(get_x_axis_values(ind), get_y_axis_values(ind), label="In-degree Distribution")
    plt.scatter(get_x_axis_values(outd), get_y_axis_values(outd), label="Out-degree Distribution")
    plt.loglog(base=10)
    plt.legend(loc=0)
    plt.title("In/Out Degree Distribution")
    plt.xlabel("Degree, k")
    plt.ylabel("Count, Nk")
    plt.savefig("graphs/dd_in_out")
    plt.clf()


def get_weakly_connected_component(graph):
    # create subgraphs for weakly connected components
    subgraphs = []
    largest_wcc = nx.path_graph(1)
    for wcc in nx.weakly_connected_components(graph):
        subgraphs.append(graph.subgraph(wcc))
        if len(wcc) > len(largest_wcc):
            largest_wcc = graph.subgraph(wcc)  # get largest weakly connected component
    # count size of subgraphs
    sizes = [g.number_of_nodes() for g in subgraphs]
    create_graph_analysis(get_x_axis_values(sizes), get_y_axis_values(sizes), "Connectivity",
                          "Weakly connected component size", "Count", "graphs/wcc.png")
    # return largest weakly connected component
    return largest_wcc


def get_strongly_connected_component(graph):
    largest_scc = graph.subgraph(max(nx.strongly_connected_components(graph), key=len))
    # return largest strongly connected component
    return largest_scc


def get_clustering_coefficient(graph):
    # get clustering coefficient and degree for each node in graph
    d = [k for n, k in graph.degree(weight='weight')]
    cc = [v for n, v in nx.clustering(graph, weight='weight').items()]
    create_graph_analysis(d, cc, "Clustering", "Degree, k", "Clustering coefficient, c", "graphs/cc.png")

    # calculate global clustering coefficient (average)
    avg_cc = nx.average_clustering(graph)
    return avg_cc


def plot_shortest_path_length(graph):
    # get lengths for each node in graph
    lengths = []
    for u in graph.nodes():
        paths = nx.single_source_dijkstra_path_length(graph, u, weight='weight')
        for p in paths:
            lengths.append(paths[p])
    create_graph_analysis(get_x_axis_values(lengths), get_y_axis_values(lengths), "Shortest Path",
                          "Shortest Path Length", "Count", "graphs/sp.png")


def get_avg_shortest_path_length(graph):
    # calculate average shortest path length using weakly_connected_component
    avg_sp = nx.average_shortest_path_length(graph, weight='weight', method='dijkstra')
    return avg_sp


def get_diameter(graph):
    # calculate diameter using strong_connected_component
    dia = nx.diameter(graph)
    return dia


if __name__ == "__main__":
    # get graph from json file
    graph = get_graph()

    # run network analysis
    print("Analyzing network...")
    get_network_analysis(graph)
    print("Network analyzed!")
