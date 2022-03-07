import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = os.path.join("comment_data", "coronavirus_all_comments.csv")
    df = pd.read_csv(path)

    authors_list = df['author'].tolist()
    df = df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]

    post_path = os.path.join("submission_data", "coronavirus_submissions.csv")
    post_df = pd.read_csv(post_path)
    post_df = post_df[['author', 'id']]

    # delete all rows that have "[deleted]" author
    df = df[df.author != "[deleted]"]
    df = df.reset_index(drop=True)
    graph = nx.DiGraph()
    # graph.add_edges_from(edgelist[author, author])
    # edge = parent_id <-> id
    # node = author
    # basically get matching parent_id and id, parent_id and link_id
    # df.loc[df["parent_id"] == "fnftok4", 'A']

    # print(df['parent_id'])
    
    l = 1
    for id in df['parent_id']:
      # if l <=10:
      parent_id = id.split('_', 1)[1]
      print('id: {}\np_id: {}'.format(post_df['id'], parent_id))
      # check for comments replying to a comment (parent_id = id)
      if (df['id'] == parent_id).any():
        # get the row where id = parent_id (direct comment)
        parent_row = df.loc[df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)
        child_rows = df.loc[df['parent_id'] == id]
        # print('p_row: {}\nc_rows: {}'.format(parent_row, child_rows))
      # check for direct comments on a post (parent_id = id)
      elif (post_df['id'] == parent_id).any():
        # get the row where id = parent_id post
        parent_row = post_df.loc[post_df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)s
        child_rows = df.loc[df['parent_id'] == id]

      # create edges and set nodes name=author
      # add_weighted_edges_from(source = child_author, target = parent_author, weight)
      for index, child_row in child_rows.iterrows():
        child_author = child_row['author']
        parent_author = parent_row['author'].iloc[0]
        # print('p_author: {}\nc_author: {}'.format(parent_author, child_author))

        # check if authors has already interacted with each other - use .has_edge(author), change the weight
        if graph.has_edge(child_author, parent_author):
          graph[child_author][parent_author]['weight'] +=1
        else : # set default weight to 1
          graph.add_weighted_edges_from([(child_author, parent_author, 1)])

      # draw and show graph after adding edges
      nx.draw(graph, node_size=10)
      plt.savefig("graph.png".format(type), bbox_inches='tight')
      plt.show()
      plt.clf() # clear canvas to show most recent graph

        # l+=1

    # TODO: analyze the graph and print into file
    print('#p_author: {}\n#c_author: {}\n#nodes: {}\n#edges: {}\nEdges: {}\n'.format(1, len(child_rows.index), graph.number_of_nodes(), graph.number_of_edges(), graph.edges.data('weight')))

    # print(df[df.author == "post_alone_musk"])

