import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import math

def get_network_analysis(graph):

  num_nodes = graph.number_of_nodes()
  num_edges = graph.number_of_edges()

  # TODO: write into file
  # print('# of nodes: {}\n# of edges: {}\nEdges: {}\n'.format(num_nodes, num_edges, graph.edges.data('weight')))

  get_node_degree_distribution(graph) # Node degree distribution
  get_weakly_connected_component(graph) # Weakly connected component
  get_clustering_coefficient(graph) # Clustering coefficient
  get_shortest_path(graph) # Shortest Path Lengths


def create_graph_analysis(x, y, title, xlabel, ylabel, file_name):
  plt.scatter(x, y)
  plt.loglog(base=10)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.savefig(file_name)
  plt.clf() 

def get_x(values):
  set_list = list(set(values)) # remove duplicates
  x = [v for v in set_list] 
  return x

def get_y(values):
  # count frequency and calculate log for y-axis
  set_list = list(set(values)) # remove duplicates
  y = [values.count(v) for v in set_list]
  return y

def get_node_degree_distribution(graph):
  # the degree is the sum of the edge weights adjacent to the node.
  # all degrees
  d = [k for n, k in graph.degree(weight='weight')]
  create_graph_analysis(get_x(d), get_y(d), "Degree Distribution", "Degree, k", "Count, Nk", "graphs/dd_all.png")

  # in degree
  ind = [k for n, k in graph.in_degree(weight='weight')]
  create_graph_analysis(get_x(ind), get_y(ind), "In Degree Distribution", "In Degree, k", "Count, Nk", "graphs/dd_in.png")

  # out degree
  outd = [k for n, k in graph.out_degree(weight='weight')]
  create_graph_analysis(get_x(outd), get_y(outd), "Out Degree Distribution", "Out Degree, k", "Count, Nk", "graphs/dd_out.png")

def get_weakly_connected_component(graph):
  # create subgraphs for weakly connected components
  subgraphs = [graph.subgraph(wcc) for wcc in nx.weakly_connected_components(graph)]
  # count size of subgraphs
  sizes = [g.number_of_nodes() for g in subgraphs]
  create_graph_analysis(get_x(sizes), get_y(sizes), "Connectivity", "Weakly connected component size", "Count", "graphs/wcc.png")

def get_clustering_coefficient(graph):
  # get clustering coefficient for each node in graph
  # the edge attribute that holds the numerical value used as a weight
  d = [k for n, k in graph.degree(weight='weight')]
  cc = [v for n, v in nx.clustering(graph, weight='weight').items()]
  create_graph_analysis(d, cc, "Clustering", "Degree, k", "Clustering coefficient, c", "graphs/cc.png")

def get_shortest_path(graph):
  # get lengths for each node in graph
  lengths = [] 
  for u in graph.nodes():
    paths = nx.single_source_shortest_path_length(graph, u)
    for p in paths:
      lengths.append(paths[p])
  create_graph_analysis(get_x(lengths), get_y(lengths), "Shortest Path", "Shortest Path Length, k", "Count", "graphs/sp.png")