import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from network_analysis import get_network_analysis 

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
    parent_row, child_rows = None, None

  return parent_row, child_rows, has_interaction

def create_edges(parent_row, child_rows):
  # add_weighted_edges_from(source = child_author, target = parent_author, weight)
  for index, child_row in child_rows.iterrows():
    child_author = child_row['author']
    parent_author = parent_row['author'].iloc[0]
    # If its a self loop, skip creating an edge to itself
    if parent_author == child_author:
      continue
    # check if authors has already interacted with each other - use .has_edge(author), change the weight
    elif graph.has_edge(child_author, parent_author):
      graph[child_author][parent_author]['weight'] += 1
    else:  # set default weight to 1
      graph.add_weighted_edges_from([(child_author, parent_author, 1)])

def create_graph():
  weights = [float(f"1.{graph[u][v]['weight']}") for u,v in graph.edges()]
  nx.draw(graph, node_size=10, width=weights)
  plt.savefig("graphs/graph.png".format(type), bbox_inches='tight')
  plt.show()
  plt.clf()  # clear canvas to show most recent graph

def filter_coc_df(coc_df):
  # delete all rows that have "[deleted]" and "AutoModerator" author
  coc_df = coc_df[~coc_df.author.isin(['[deleted]', 'AutoModerator'])]
  coc_df = coc_df.reset_index(drop=True)
  return coc_df

def get_df():
  coc_path = os.path.join("comment_data", "coronavirus_all_comments.csv")
  coc_df = pd.read_csv(coc_path)
  coc_df = coc_df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]

  post_path = os.path.join("submission_data", "coronavirus_submissions.csv")
  post_df = pd.read_csv(post_path)
  post_df = post_df[['author', 'id']]

  return coc_df, post_df

if __name__ == "__main__":
  # get 'Comment On Comment Dataframe' and 'Post Dataframe'
  coc_df, post_df = get_df()
  authors_list = coc_df['author'].tolist()

  coc_df = filter_coc_df(coc_df)
  graph = nx.DiGraph()
  
  # l = 1
  print("Creating edges...")
  for id in coc_df['parent_id']:
    # if l <= 10:
      parent_id = id.split('_', 1)[1]
      has_interaction = True
      parent_row, child_rows, has_interaction = set_interaction(id, parent_id,
                                                                coc_df, post_df,
                                                                has_interaction)

      if has_interaction:
        # create edges and set nodes name=author
        create_edges(parent_row, child_rows)
      # l += 1
  print("Edges created!")
  
  # draw and show graph after adding edges 
  # (can skip this step after running it once to save time)
  print("Creating graph...")
  create_graph()
  print("Graph created!")

  # TODO: analyze the graph with more data and print into file
  print("Analzing network...")
  get_network_analysis(graph)
  print("Network analyzed!")