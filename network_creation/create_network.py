import os

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from created_network import save_graph
from data_preprocess_ops.filter_comments import filter_comments
from definitions import ROOT_DIR
from network_creation.bipartite_graph import create_bipartite_graph


def set_interaction(id, parent_id, comments_df, submissions_df, has_interaction):
    # check for comments replying to a comment (parent_id = id)
    if (comments_df['id'] == parent_id).any():
        # get the row where id = parent_id (user receiving the comment)
        parent_row = comments_df.loc[comments_df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)
        child_rows = comments_df.loc[comments_df['parent_id'] == id]
    # check for direct comments on a post (parent_id = id)
    elif (submissions_df['id'] == parent_id).any():
        # get the row where id = parent_id post
        parent_row = submissions_df.loc[submissions_df['id'] == parent_id]
        # get all rows where parent_id = parent_id (reply to someone's a comment)s
        child_rows = comments_df.loc[comments_df['parent_id'] == id]
    else:
        # node has no data for parent_id = id, hence don't create edge
        has_interaction = False
        parent_row, child_rows = None, None

    return parent_row, child_rows, has_interaction


def create_graph(comments_df, submissions_df):
    # get unique set of parent_ids
    parent_ids = set(comments_df['parent_id'])

    graph = nx.DiGraph()

    for id in parent_ids:
        parent_id = id.split('_', 1)[1]
        has_interaction = True
        parent_row, child_rows, has_interaction = set_interaction(id, parent_id,
                                                                  comments_df, submissions_df,
                                                                  has_interaction)

        if has_interaction:
            # create edges and set nodes name=author
            create_edges(graph, parent_row, child_rows)
    return graph


def create_edges(graph, parent_row, child_rows):
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
        # use .has_edge(child_author, parent_author), change the weight and append comment
        elif graph.has_edge(child_author, parent_author):
            weight = graph[child_author][parent_author]['weight']
            comments = list(graph[child_author][parent_author]['comments'])
            comments.append(child_comment)
            graph.add_edge(child_author, parent_author, weight=weight + 1, comments=comments)
        else:  # set default weight to 1, set comment from child author in edge
            graph.add_edge(child_author, parent_author, weight=1, comments=comments)
            comments.append(child_comment)


def draw_graph(graph, filename):
    plt.figure(figsize=(150, 150), dpi=50)
    weights = [float(f"{graph[u][v]['weight']}") for u, v in graph.edges()]
    nx.draw(graph, node_size=300, width=weights)
    plt.show()
    plt.savefig(os.path.join(ROOT_DIR, "graphs", filename), bbox_inches='tight')
    plt.clf()  # clear canvas to show most recent graph
    plt.figure(figsize=(8.0, 6.0), dpi=80)  # reset to default size


def filter_comments_df(comments_df):
    num_comments_before = len(comments_df)
    # delete all rows that have "[deleted]" and "AutoModerator" author
    comments_df = comments_df[~comments_df.author.isin(['[deleted]', 'AutoModerator'])]
    comments_df = comments_df.reset_index(drop=True)
    # filter out comments and remove duplicate comments
    ignored_text = ["Your post or comment has been removed", "Microsoft SQL server"]
    comments_df = filter_comments(comments_df, 'body', ignored_text)
    comments_df = comments_df.drop_duplicates(subset=['body'], keep='first')
    num_comments_after = len(comments_df)
    return comments_df, num_comments_before, num_comments_after


def filter_submissions_df(df):
    df = df[~df.author.isin(['[deleted]', 'AutoModerator'])]
    df = df.reset_index(drop=True)
    return df


def get_df():
    comments_path = os.path.join(ROOT_DIR, "data_collection", "coronavirus_comments.csv")
    comments_df = pd.read_csv(comments_path,
                              dtype={"author": "string", "id": "string", "link_id": "string", "parent_id": "string",
                                     "body": "string"})
    comments_df = comments_df[['author', 'id', 'link_id', 'parent_id', 'body']]

    submissions_path = os.path.join(ROOT_DIR, "data_collection", "coronavirus_submissions.csv")
    submissions_df = pd.read_csv(submissions_path, dtype={"author": "string", "id": "string"})
    submissions_df = submissions_df[['author', 'id']]

    return comments_df, submissions_df


def save_comments_stats(filename, num_comments_before, num_comments_after):
    # write number of comments to stats file
    before_after_dict = {'Statistics': ['Before filtering', 'After filtering'],
                         'Number of comments': [num_comments_before, num_comments_after]}
    before_row_dict = {'Statistics': ['Before filtering'], 'Number of comments': [num_comments_before]}
    after_row_dict = {'Statistics': ['After filtering'], 'Number of comments': [num_comments_after]}

    if os.path.exists(filename):
        # read existing csv file
        df = pd.read_csv(filename)
        if (df['Statistics'] == 'Before filtering').any() and (df['Statistics'] == 'After filtering').any():
            # update data
            df.loc[df.loc[df['Statistics'] == 'Before filtering'].index[0], 'Number of comments'] = num_comments_before
            df.loc[df.loc[df['Statistics'] == 'After filtering'].index[0], 'Number of comments'] = num_comments_after
        else:
            # add data
            df = pd.concat([df, pd.DataFrame(before_row_dict)], ignore_index=True)
            df = pd.concat([df, pd.DataFrame(after_row_dict)], ignore_index=True)
    else:
        # create csv file if file doesn't exist
        df = pd.DataFrame(before_after_dict)

    # writing into the file
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    # get 'Comments Data frame' and 'Submissions Data frame'
    comments_df, submissions_df = get_df()
    authors_list = comments_df['author'].tolist()

    # filter comments
    comments_df, num_comments_before, num_comments_after = filter_comments_df(comments_df)
    submissions_df = filter_submissions_df(submissions_df)
    # save comment statistics
    save_comments_stats(ROOT_DIR + "/csv_data/comments_stats.csv", num_comments_before, num_comments_after)

    print("Creating graph...")
    user_social_network_graph = create_graph(comments_df, submissions_df)
    print("Graph created!")

    # draw and show graph after adding edges
    # (can skip this step after running it once to save time)
    print("Drawing graph...")
    draw_graph(user_social_network_graph, "user_social_network_graph.png")
    print("Graph drew!")

    print("Saving graph...")
    # save graph in file
    save_graph(user_social_network_graph, "user_social_network")
    print("Graph saved!")

    df = pd.read_csv(os.path.join(ROOT_DIR, "csv_data", "author_topic_sentiment.csv"),
                     dtype={"author": str, "topic": int, "avg_score": float})
    print("Creating bipartite graph...")
    user_to_topic_graph, set1_nodes, set2_nodes = create_bipartite_graph(df)
    print("Bipartite Graph created!")
    # TODO: refactor drawing into method and make better image
    plt.figure(figsize=(150, 150), dpi=50)
    nx.draw_networkx(user_to_topic_graph, node_size=300,
                     pos=nx.drawing.bipartite_layout(user_to_topic_graph, set1_nodes))
    plt.savefig(os.path.join(ROOT_DIR, "graphs", "user_to_topic_graph.png"), bbox_inches='tight')
    print("Saving Bipartite graph...")
    save_graph(user_to_topic_graph, "user_to_topic")
    print("Bipartite graph saved!")