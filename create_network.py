import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from network_analysis import get_network_analysis


def set_interaction(id, parent_id, comments_df, posts_df, has_interaction):
    # check for comments replying to a comment (parent_id = id)
    if (comments_df['id'] == parent_id).any():
        # get the row where id = parent_id (user receiving the comment)
        parent_row = comments_df.loc[comments_df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)
        child_rows = comments_df.loc[comments_df['parent_id'] == id]
    # check for direct comments on a post (parent_id = id)
    elif (posts_df['id'] == parent_id).any():
        # get the row where id = parent_id post
        parent_row = posts_df.loc[posts_df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)s
        child_rows = comments_df.loc[comments_df['parent_id'] == id]
    else:
        # node has no data for parent_id = id, hence don't create edge
        has_interaction = False
        parent_row, child_rows = None, None

    return parent_row, child_rows, has_interaction


def create_edges(parent_row, child_rows):
    # add_weighted_edges_from(source = child_author, target = parent_author, weight)
    for index, child_row in child_rows.iterrows():
        parent_author = parent_row['author'].iloc[0]
        child_author = child_row['author']
        child_comment = child_row['body']
        comments = []
        # If its a self loop, skip creating an edge to itself
        if parent_author == child_author:
            continue
        # check if authors has already interacted with each other 
        # use .has_edge(author), change the weight and append comment
        elif graph.has_edge(child_author, parent_author):
            graph[child_author][parent_author]['weight'] += 1
            comments = list(graph[child_author][parent_author]['comments'])
            # print("created before append ({},{}) comments={} comcom={}".format(child_author, parent_author, len(comments), comments))
            comments.append(child_comment)
            nx.set_edge_attributes(graph, {(child_author, parent_author): {"comments": comments}})
            # print("created after append ({},{}) comments={} comcom={}".format(child_author, parent_author, len(comments), comments))
        else: # set default weight to 1, set comment from child author in edge
            graph.add_weighted_edges_from([(child_author, parent_author, 1)])
            comments.append(child_comment)
            nx.set_edge_attributes(graph, {(child_author, parent_author): {"comments": comments}})
            # print("not created ({},{}) comments={}".format(child_author, parent_author, len(comments)))

def create_graph():
    weights = [float(f"1.{graph[u][v]['weight']}") for u, v in graph.edges()]
    nx.draw(graph, node_size=10, width=weights)
    plt.savefig("graphs/graph.png".format(type), bbox_inches='tight')
    plt.show()
    plt.clf()  # clear canvas to show most recent graph


def filter_comments_df(comments_df):
    # delete all rows that have "[deleted]" and "AutoModerator" author
    comments_df = comments_df[~comments_df.author.isin(['[deleted]', 'AutoModerator'])]
    comments_df = comments_df.reset_index(drop=True)
    return comments_df


def get_df():
    coc_path = os.path.join("comment_data", "coronavirus_all_comments.csv")
    comments_df = pd.read_csv(coc_path)
    comments_df = comments_df[['author', 'id', 'link_id', 'parent_id', 'subreddit_id', 'body']]

    post_path = os.path.join("submission_data", "coronavirus_submissions.csv")
    posts_df = pd.read_csv(post_path)
    posts_df = posts_df[['author', 'id']]

    return comments_df, posts_df


if __name__ == "__main__":
    # get 'Comments Data frame' and 'Posts Data frame'
    comments_df, posts_df = get_df()
    authors_list = comments_df['author'].tolist()

    comments_df = filter_comments_df(comments_df)
    # get unique set of parent_ids
    parent_ids = set(comments_df['parent_id'])

    graph = nx.DiGraph()

    print("Creating edges...")
    for id in parent_ids:
        parent_id = id.split('_', 1)[1]
        has_interaction = True
        parent_row, child_rows, has_interaction = set_interaction(id, parent_id,
                                                                  comments_df, posts_df,
                                                                  has_interaction)

        if has_interaction:
            # create edges and set nodes name=author
            create_edges(parent_row, child_rows)
    print("Edges created!")

    # draw and show graph after adding edges
    # (can skip this step after running it once to save time)
    print("Creating graph...")
    create_graph()
    print("Graph created!")

    # TODO: analyze the graph with more data and print into file
    print("Analyzing network...")
    get_network_analysis(graph)
    print("Network analyzed!")
