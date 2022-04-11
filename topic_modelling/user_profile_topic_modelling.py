import os

import pandas as pd

from LDA_topic_modelling import topic_modelling
from data_preprocess_ops.preprocess_documents import preprocess_documents


# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def extract_documents(filename):
    comments_df = pd.read_csv(filename, dtype={"author": "string", "body": "string"})
    comments_df = comments_df[['author', 'body']]
    comments_df = comments_df.sort_values(by=['author'], ascending=True)
    return comments_df


def get_unique_authors(df):
    return df["author"].unique()


def get_top_k_frequent_authors(df, k):
    authors = df['author'].value_counts()[:k].index.tolist()
    return filter_authors(authors)


def filter_authors(authors):
    ignored_authors = set(["[deleted]", "AutoModerator"])
    filtered_authors = list(filter(lambda author: author not in ignored_authors, authors))
    return filtered_authors


def get_all_tokens_by_user(df, user):
    all_tokens_by_user = df[df['author'] == user]
    return all_tokens_by_user['tokens'].tolist()


def get_user_topics(user):
    documents = pd.read_csv("preprocessed_documents.csv")
    author_tokens = get_all_tokens_by_user(documents, user)
    return topic_modelling(author_tokens, num_topics=5, passes=4, user=user)


if __name__ == "__main__":
    filename = os.path.join("../comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)

    # download_nltk_files() # Run only once

    documents = preprocess_documents(documents)
    # get top 10 most frequent names
    n = 10
    authors = get_top_k_frequent_authors(documents, n)

    # authors = get_unique_authors(documents)
    print(f"Unique authors: {len(authors)}")

    for author in authors:
        print(author)
        author_tokens = get_all_tokens_by_user(documents, author)

        print(f"Author_tokens: {author_tokens}")

        topic_modelling(author_tokens, num_topics=5, passes=4)
