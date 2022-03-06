import os
import networkx as nx
import pandas as pd

if __name__ == "__main__":
    path = os.path.join("comment_data", "coronavirus_all_comments.csv")
    df = pd.read_csv(path)

    authors_list = df['author'].tolist()
    df = df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]

    # delete all rows that have "[deleted]" author
    df = df[df.author != "[deleted]"]
    df = df.reset_index(drop=True)
    graph = nx.Graph()
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
        print('p_id: {}'.format(parent_id))
        # get all rows where parent_id = parent_id (reply to someone's a comment)
        childs_rows = df.loc[df['parent_id'] == parent_id]
        # check if id == parent_id
        if (df['id'] == parent_id).any():
          # get the row where id = parent_id (direct comment)
          parent_row = df.loc[df['id'] == parent_id]
          print('c_author: {}\np_author: {}'.format(childs_rows, parent_row))
        l+=1



    # print(df[df.author == "post_alone_musk"])

