import ast
import collections
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from definitions import ROOT_DIR
from topic_modelling.user_profile_topic_modelling import get_unique_authors, filter_authors


def get_author_topic_distribution(df):
    # (x, y) = {'topic': {authors}}
    # {authors} = [author1, author2, author3]
    # x = topic, y = length of authors 
    topic_authors_dict = collections.defaultdict(set)
    for index, row in df.iterrows():
        topic = row['topic']
        author = row['author']
        topic_authors_dict[topic].add(author)
    # take length of authors
    # x = topic, y = number of authors
    topic_authors_length = {}
    for key in topic_authors_dict:
        topic_authors_length[key] = len(topic_authors_dict[key])
    return topic_authors_length


def get_comment_topic_distribution(df):
    # (x, y) = {'topic': number of comments}
    # x = topic, y = number of comments
    topic_comments_dict = {}
    for index, row in df.iterrows():
        # TODO: Remove regex stuff
        topic = re.split(',', str(row['topic']))[0][1:]
        sentiment = re.split(', |\'', str(row['sentiment']))[1]
        if topic != "an":  # filter out "Nan" topics
            if topic in topic_comments_dict:
                topic_comments_dict[topic][sentiment] += 1
                topic_comments_dict[topic]["total"] += 1
            else:
                if sentiment == "pos":
                    topic_comments_dict[topic] = {"pos": 1, "neu": 0, "neg": 0, "total": 1}
                elif sentiment == "neu":
                    topic_comments_dict[topic] = {"pos": 0, "neu": 1, "neg": 0, "total": 1}
                else:
                    topic_comments_dict[topic] = {"pos": 0, "neu": 0, "neg": 1, "total": 1}

    # write number of comments to stats file
    num_comments = 0
    for x in list(topic_comments_dict.values()):
        num_comments += x["total"]
    f = open("comments_stats.txt", "a")
    f.write(f"\n# of comments with topic: {num_comments}")
    f.close()

    return topic_comments_dict


def plot_distribution(data, title, xlabel, ylabel, file_name):
    data.plot(x=xlabel, y=ylabel, kind="bar", title=title, xlabel=xlabel, ylabel=ylabel, legend=False)
    plt.savefig(file_name)
    plt.clf()
    return


def plot_sent_distribution(x, y_pos, y_neu, y_neg, title, xlabel, ylabel, file_name):
    width = 0.25
    x_axis = np.arange(len(x))
    plt.bar(x_axis - width, y_pos, width=width, label="Positive", color="green")
    plt.bar(x_axis, y_neu, width=width, label="Neutral", color="blue")
    plt.bar(x_axis + width, y_neg, width=width, label="Negative", color="red")
    plt.xticks(x_axis + width / 3, x)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(file_name)
    plt.clf()
    return


# def filter_topics(row):


# TODO: Refactor this function/remove regex stuff after re-formatting processed_documents.csv
# TODO: author <-> topic, sentiment
def get_author_topic_sentiment(df):
    authors = get_unique_authors(df)
    unique_authors = filter_authors(authors)
    author_topic_sentiment_data = []
    for author in unique_authors:
        author_df = df.loc[df['author'] == author]
        unique_topics_ids = author_df['topic'].unique()

        for topic_id in unique_topics_ids:
            author_to_topic_row = author_df[author_df['topic'] == topic_id]
            # print(author_to_topic_row)
            # Take the average score of all these rows
            total_sentiment_score = 0
            for _, author_row in author_to_topic_row.iterrows():
                total_sentiment_score += author_row['sentiment'][1]

            average_sentiment_score = total_sentiment_score / len(author_to_topic_row)
            author_topic_sentiment_data.append([author, topic_id, average_sentiment_score])
    author_topic_sentiment = pd.DataFrame(author_topic_sentiment_data, columns=["author", "topic", "avg_score"])
    return author_topic_sentiment


if __name__ == "__main__":
    topic_modelling_path = os.path.join(ROOT_DIR, "processed_documents.csv")

    df = pd.read_csv(topic_modelling_path)
    df = df[['author', 'body', 'topic', 'sentiment']]
    df = df.dropna(subset=['topic'])
    df['topic'] = df['topic'].apply(ast.literal_eval)
    df['topic'] = df['topic'].apply(lambda x: x[0])
    df['sentiment'] = df['sentiment'].apply(ast.literal_eval)

    topic_authors_dict = get_author_topic_distribution(df)

    # convert to dataframe to sort by total number of comments
    topic_authors_df = pd.DataFrame(topic_authors_dict.items(), columns=["Topics", "Number of Unique Authors"])
    topic_authors_df = topic_authors_df.sort_values("Number of Unique Authors", ascending=False)

    # print(topic_authors_df)
    # # plot author vs topic distribution
    plot_distribution(topic_authors_df, "Topics Discussed by Authors", "Topics", "Number of Unique Authors",
                      os.path.join(ROOT_DIR, "graphs", "topic_authors.png"))

    # # comment vs topic distribution
    # topic_comments_dict = get_comment_topic_distribution(df)

    # topic_comments_dict_x_axis = list(topic_comments_dict.keys())

    # # without sentiment
    # total_topic_comments_dict_y_axis = [x["total"] for x in list(topic_comments_dict.values())]
    # # with sentiment
    # sent_pos_topic_comments_dict_y_axis = [x["pos"] for x in list(topic_comments_dict.values())]
    # sent_neu_topic_comments_dict_y_axis = [x["neu"] for x in list(topic_comments_dict.values())]
    # sent_neg_topic_comments_dict_y_axis = [x["neg"] for x in list(topic_comments_dict.values())]
    # # convert to dataframe to sort by total number of comments
    # topic_comments_df = pd.DataFrame({"Topics": topic_comments_dict_x_axis, "Number of Comments": total_topic_comments_dict_y_axis, "Positive": sent_pos_topic_comments_dict_y_axis, "Neutral": sent_neu_topic_comments_dict_y_axis, "Negative": sent_neg_topic_comments_dict_y_axis})
    # topic_comments_df= topic_comments_df.sort_values("Number of Comments", ascending=False)

    # # plot comment vs topic distribution without sentiment
    # plot_distribution(topic_comments_df, "Topics Discussed in Comments", "Topics", "Number of Comments", "graphs/topic_comments.png")
    # # plot comment vs topic distribution with sentiment
    # plot_sent_distribution(topic_comments_df["Topics"].tolist(), topic_comments_df["Positive"].tolist(), topic_comments_df["Neutral"].tolist(), topic_comments_df["Negative"].tolist(), "Sentiments Towards Topics Discussed in Comments", "Topics", "Number of Comments", "graphs/topic_comments_sentiment.png")

    # create author to topic bipartite graph
    # author_topic_sentiment_df = get_author_topic_sentiment(df)

    # write dataframes to files
    # topic_authors_df.to_csv("topic_authors_distribution.csv", index=False)
    # topic_comments_df.to_csv("topic_comments_distribution.csv", index=False)
    # author_topic_sentiment_df.to_csv("author_topic_sentiment.csv", index=False)
