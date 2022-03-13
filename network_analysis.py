import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import csv

def get_network_analysis(graph):

  num_nodes = graph.number_of_nodes() # of nodes
  num_edges = graph.number_of_edges() # of edges
  get_node_degree_distribution(graph) # Node degree distribution
  avg_cc = get_clustering_coefficient(graph) # Clustering coefficient / average clustering coefficient
  avg_sp, num_nodes_weak, num_edges_weak = get_shortest_path_length(graph) # Shortest path engths / average shortest path length
  get_weakly_connected_component(graph) # Weakly connected component
  dia, num_nodes_strong, num_edges_strong = get_diameter(graph) # Diameter

  with open('network_analysis.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    component_type = ['All Components', 'Weakly Connected Component', 'Strongly Connected Component']
    
    ac_header = ['Num of Nodes', 'Num of Edges','Global Clustering Coefficient']
    ac_data = [num_nodes, num_edges, avg_cc]
    writer.writerow([component_type[0]])
    writer.writerow(ac_header)
    writer.writerow(ac_data)

    wcc_header = ['Num of Nodes', 'Num of Edges', 'Average Shortest Path']
    wcc_data = num_nodes_weak, num_edges_weak, avg_sp
    writer.writerow([component_type[1]])
    writer.writerow(wcc_header)
    writer.writerow(wcc_data)

    scc_header = ['Num of Nodes', 'Num of Edges', 'Diameter']
    scc_data = num_nodes_strong, num_edges_strong, dia
    writer.writerow([component_type[2]])
    writer.writerow(scc_header)
    writer.writerow(scc_data)

def create_graph_analysis(x, y, title, xlabel, ylabel, file_name):
  plt.scatter(x, y)
  plt.loglog(base=10)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.savefig(file_name)
  plt.clf() 

def get_x_axis_values(values):
  x_axis_values = list(set(values)) # remove duplicates
  return x_axis_values

def get_y_axis_values(values):
  # count frequency and calculate log for y-axis
  y_axis_values = [values.count(v) for v in get_x_axis_values(values)]
  return y_axis_values

def get_node_degree_distribution(graph):
  # the degree is the sum of the edge weights adjacent to the node.
  # all degrees
  d = [k for n, k in graph.degree(weight='weight')]
  create_graph_analysis(get_x_axis_values(d), get_y_axis_values(d), "Degree Distribution", "Degree, k", "Count, Nk", "graphs/dd_all.png")

  # in-degrees
  ind = [k for n, k in graph.in_degree(weight='weight')]
  create_graph_analysis(get_x_axis_values(ind), get_y_axis_values(ind), "In Degree Distribution", "In Degree, k", "Count, Nk", "graphs/dd_in.png")

  # out-degrees
  outd = [k for n, k in graph.out_degree(weight='weight')]
  create_graph_analysis(get_x_axis_values(outd), get_y_axis_values(outd), "Out Degree Distribution", "Out Degree, k", "Count, Nk", "graphs/dd_out.png")

def get_weakly_connected_component(graph):
  # create subgraphs for weakly connected components
  subgraphs = [graph.subgraph(wcc) for wcc in nx.weakly_connected_components(graph)]
  # count size of subgraphs
  sizes = [g.number_of_nodes() for g in subgraphs]
  create_graph_analysis(get_x_axis_values(sizes), get_y_axis_values(sizes), "Connectivity", "Weakly connected component size", "Count", "graphs/wcc.png")

def get_clustering_coefficient(graph):
  # get clustering coefficient and degree for each node in graph
  d = [k for n, k in graph.degree(weight='weight')]
  cc = [v for n, v in nx.clustering(graph, weight='weight').items()]
  create_graph_analysis(d, cc, "Clustering", "Degree, k", "Clustering coefficient, c", "graphs/cc.png")

  # calculate global clustering coefficient (average)
  avg_cc = nx.average_clustering(graph)
  return avg_cc

def get_shortest_path_length(graph):
  # get lengths for each node in graph
  lengths = [] 
  for u in graph.nodes():
    paths = nx.single_source_dijkstra_path_length(graph, u, weight='weight')
    for p in paths:
      lengths.append(paths[p])
  create_graph_analysis(get_x_axis_values(lengths), get_y_axis_values(lengths), "Shortest Path", "Shortest Path Length", "Count", "graphs/sp.png")
  
  # calculate average shortest path length
  giant_component = graph.subgraph(max(nx.weakly_connected_components(graph), key=len))
  num_nodes = giant_component.number_of_nodes()
  num_edges = giant_component.number_of_edges()
  avg_sp = nx.average_shortest_path_length(giant_component, weight='weight', method='dijkstra')
  return avg_sp, num_nodes ,num_edges

def get_diameter(graph):
  # calculate diameter
  giant_component = graph.subgraph(max(nx.strongly_connected_components(graph), key=len))
  num_nodes = giant_component.number_of_nodes()
  num_edges = giant_component.number_of_edges()
  dia = nx.diameter(giant_component)
  return dia, num_nodes, num_edges