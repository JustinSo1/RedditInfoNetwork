import os
import networkx as nx
import pandas as pd

if __name__ == "__main__":
    path = os.path.join("comment_data","coronavirus_all_comments.csv")
    df = pd.read_csv(path)

    authors_list = df['author'].tolist()
    df = df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id']]
    
    # delete all rows that have "[deleted]" author
    df = df[df.author != "[deleted]"]

    print(df)
