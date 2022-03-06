import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = os.path.join("comment_data", "coronavirus_all_comments.csv")
    df = pd.read_csv(path)

    authors_list = df['author'].tolist()
    df = df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]

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
      if l <=10:
        parent_id = id.split('_', 1)[1]
        # print('p_id: {}'.format(parent_id))
        # check if id == parent_id
        if (df['id'] == parent_id).any():
          # get the row where id = parent_id (direct comment)
          parent_row = df.loc[df['id'] == parent_id]
          # get all rows where parent_id = parent_id (reply to someone's a comment)
          child_rows = df.loc[df['parent_id'] == id]
          # print('p_row: {}\nc_rows: {}'.format(parent_row, child_rows))

          
          
          # create edges and set nodes name=author
          for index, child_row in child_rows.iterrows():
            # (source = child_author, target = parent_author, weight)
            child_author = child_row['author']
            parent_author = parent_row['author'].iloc[0]
            print('p_author: {}\nc_author: {}'.format(parent_author, child_author))

            # TODO: check if authors has already interacted with each other - use .has_node(author), change the weight

            # else set default weight to 1
            graph.add_weighted_edges_from([(child_author, parent_author, 1)])


        nx.draw(graph, node_size=10)
        plt.savefig("graph.png".format(type), bbox_inches='tight')
        plt.show()

        l+=1



    # print(df[df.author == "post_alone_musk"])

