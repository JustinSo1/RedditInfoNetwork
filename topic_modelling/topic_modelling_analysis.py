import os
import pandas as pd
import matplotlib.pyplot as plt
import re

def get_author_topic_distribution(df):
    # (x, y) = ('topic': {authors})
    # {authors} = [author1, author2, author3]
    # x = topic, y = length of authors 
    topic_authors_dict = {}
    for index, row in df.iterrows():
        topic = re.split(',', str(row['topic']))[0][1:]
        if topic != "an": # filter out "Nan" topics
            author = row['author']
            if topic in topic_authors_dict:
                if author not in topic_authors_dict[topic]:
                    topic_authors_dict[topic].append(author)
            else:
                topic_authors_dict[topic] = [author]
    # take length of authors
    # x = topic, y = number of authors
    for key in topic_authors_dict.keys():
        topic_authors_dict[key] = len(topic_authors_dict[key]) 

    return topic_authors_dict

def get_comment_topic_distribution(df):
    # (x, y) = ('topic': number of comments)
    # x = topic, y = number of comments
    topic_comments_dict = {}
    for index, row in df.iterrows():
        topic = re.split(',', str(row['topic']))[0][1:]
        if topic != "an": # filter out "Nan" topics
            if topic in topic_comments_dict:
                topic_comments_dict[topic] += 1
            else:
                topic_comments_dict[topic] = 1

    num_comments = 0
    for x in list(topic_comments_dict.values()):
      num_comments+=x
    f = open("comments_stats.txt", "a")
    f.write(f"# of comments with topic: {num_comments}\n")
    f.close()
    return topic_comments_dict

def plot_distribution(data, title, xlabel, ylabel, file_name):
    print(data)
    plt.bar(xlabel, ylabel, data=data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(file_name)
    plt.clf()
    return

if __name__ == "__main__":
    topic_modelling_path = os.path.join("processed_documents.csv")
    df = pd.read_csv(topic_modelling_path)
    df = df[['author', 'body', 'topic']]

    # plot author vs topic distribution
    topic_authors_dict = get_author_topic_distribution(df)
    topic_authors_dict_x_axis = list(topic_authors_dict.keys())
    topic_authors_dict_y_axis = list(topic_authors_dict.values())
    topic_authors_df = pd.DataFrame({"Topics": topic_authors_dict_x_axis, "Number of Unique Authors": topic_authors_dict_y_axis})
    topic_authors_df= topic_authors_df.sort_values("Number of Unique Authors", ascending=False)
    plot_distribution(topic_authors_df, "Topics Discussed by Authors", "Topics", "Number of Unique Authors", "graphs/topic_authors.png")
    
    # plot comment vs topic distribution
    topic_comments_dict = get_comment_topic_distribution(df)
    topic_comments_dict_x_axis = list(topic_comments_dict.keys())
    topic_comments_dict_y_axis = list(topic_comments_dict.values())
    topic_comments_df = pd.DataFrame({"Topics": topic_comments_dict_x_axis, "Number of Comments": topic_comments_dict_y_axis})
    topic_comments_df= topic_comments_df.sort_values("Number of Comments", ascending=False)
    plot_distribution(topic_comments_df, "Topics Discussed in Comments", "Topics", "Number of Comments", "graphs/topic_comments.png")
