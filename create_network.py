import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def set_interaction(id, parent_id, coc_df, post_df, has_interaction):
  # check for comments replying to a comment (parent_id = id)
  if (coc_df['id'] == parent_id).any():
    # get the row where id = parent_id (user receiving the comment)
    parent_row = coc_df.loc[coc_df['id'] == parent_id]
    # get all rows where parent_id = parent_id (reply to someone's a comment)
    child_rows = coc_df.loc[coc_df['parent_id'] == id]
  # check for direct comments on a post (parent_id = id)
  elif (post_df['id'] == parent_id).any():
    # get the row where id = parent_id post
    parent_row = post_df.loc[post_df['id'] == parent_id]
    # get all rows where parent_id = parent_id (reply to someone's a comment)s
    child_rows = coc_df.loc[coc_df['parent_id'] == id]
  else:
    # node has no data for parent_id = id, hence don't create edge
    has_interaction = False

  return parent_row, child_rows, has_interaction

def create_edges(parent_row, child_rows):
  # add_weighted_edges_from(source = child_author, target = parent_author, weight)
  for index, child_row in child_rows.iterrows():
    child_author = child_row['author']
    parent_author = parent_row['author'].iloc[0]
    # check if authors has already interacted with each other - use .has_edge(author), change the weight
    if graph.has_edge(child_author, parent_author):
      graph[child_author][parent_author]['weight'] +=1
    else : # set default weight to 1
      graph.add_weighted_edges_from([(child_author, parent_author, 1)])

def create_graph():
  nx.draw(graph, node_size=10)
  plt.savefig("graphs/graph.png".format(type), bbox_inches='tight')
  plt.show()
  plt.clf() # clear canvas to show most recent graph

def filter_coc_df(coc_df):
  # delete all rows that have "[deleted]" and "AutoModerator" author
  coc_df = coc_df[coc_df.author != "[deleted]"]
  coc_df = coc_df[coc_df.author != "AutoModerator"]
  coc_df = coc_df.reset_index(drop=True)

def get_df():
  path = os.path.join("comment_data", "coronavirus_all_comments.csv")
  coc_df = pd.read_csv(path)
  coc_df = coc_df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]

  post_path = os.path.join("submission_data", "coronavirus_submissions.csv")
  post_df = pd.read_csv(post_path)
  post_df = post_df[['author', 'id']]

  return coc_df, post_df

def get_graph_analysis():

  get_node_degree_distribution() # Node degree distribution
  get_weakly_connected_component() # Weakly connected component

  # print('#p_author: {}\n#c_author: {}\n#nodes: {}\n#edges: {}\nEdges: {}\n'.format(1, len(child_rows.index), graph.number_of_nodes(), graph.number_of_edges(), graph.edges.data('weight')))

def create_graph_analysis(graph_values, title, xlabel, ylabel, file_name):
  plt.hist(graph_values)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.savefig(file_name)
  plt.clf() 

def get_node_degree_distribution():
  # The degree is the sum of the edge weights adjacent to the node.
  # TODO: change to plot log-log scatter plot
  # all degrees
  d = [k for n, k in graph.degree(weight='weight')]
  # x-axis
  x = []
  for v in d:
    if v not in x:
      x.append(v)
  # y-axis
  y = [d.count(v) for v in x]
  print(x, y)

  create_graph_analysis(d, "Degree Distribution", "Degree, k", "Count, Nk", "graphs/dd_all.png")

  # in degree
  ind = d = [k for n, k in graph.in_degree(weight='weight')]
  create_graph_analysis(ind, "In Degree Distribution", "In Degree, k", "Count, Nk", "graphs/dd_in.png")

  # out degree
  outd = [k for n, k in graph.out_degree(weight='weight')]
  create_graph_analysis(outd, "Out Degree Distribution", "Out Degree, k", "Count, Nk", "graphs/dd_out.png")

def get_weakly_connected_component():
  
  create_graph_analysis("outd", "Out Degree Distribution", "Out Degree, k", "Count, Nk", "graphs/dd_out.png")
  return {}

if __name__ == "__main__":

    # get 'Comment On Comment Dataframe' and 'Post Dataframe' 
    coc_df, post_df = get_df()
    authors_list = coc_df['author'].tolist()

    filter_coc_df(coc_df)
    graph = nx.DiGraph()
    
    l = 1
    for id in coc_df['parent_id']:
      if l <= 10:
        parent_id = id.split('_', 1)[1]
        has_interaction = True
        parent_row, child_rows = set_interaction(id, parent_id, coc_df, post_df, has_interaction)

        if has_interaction:
          # create edges and set nodes name=author
          create_edges(parent_row, child_rows)

        l += 1
    
    # draw and show graph after adding edges
    create_graph()

    # TODO: analyze the graph and print into file
    get_graph_analysis()