import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import math

def get_network_analysis(graph):

  # TODO: write into file
  # print('#nodes: {}\n#edges: {}\nEdges: {}\n'.format(graph.number_of_nodes(), graph.number_of_edges(), graph.edges.data('weight')))

  get_node_degree_distribution(graph) # Node degree distribution
  get_weakly_connected_component(graph) # Weakly connected component

  # TODO: local clustering coefficient - look into if this is done correctly
  # do we also want to include average (global) clustering coefficient?
  get_clustering_coefficient(graph) # Local clustering coefficient


def create_graph_analysis(x, y, title, xlabel, ylabel, file_name):
  plt.scatter(x, y)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.savefig(file_name)
  plt.clf() 

def get_x(values):
  # calculate log for x-axis
  set_list = list(set(values)) # remove duplicates
  x = [math.log(v) if v != 0 else 0 for v in set_list] 
  return x

def get_y(values):
  # count frequency and calculate log for y-axis
  set_list = list(set(values)) # remove duplicates
  y = [math.log(values.count(v)) for v in set_list]
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
  create_graph_analysis(get_x(sizes), get_y(sizes), "Weakly Connected Component", "Weakly connected component size", "Count", "graphs/wcc.png")

def get_clustering_coefficient(graph):
  # get clustering coefficient for each node in graph
  # the edge attribute that holds the numerical value used as a weight
  cc = [v for n, v in nx.clustering(graph, weight='weight').items()]
  create_graph_analysis(get_x(cc), get_y(cc), "Local Clustering Coefficient", "Clustering coefficient, c", "Count", "graphs/cc.png")