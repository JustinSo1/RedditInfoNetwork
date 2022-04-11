import os

import pandas as pd

from topic_modelling.user_profile_topic_modelling import get_user_topics, filter_authors


def get_unique_authors(df):
    return df["author"].unique()


if __name__ == "__main__":
    # filename = os.path.join("Topic_Distribution.csv")
    # user_topics = pd.read_csv(filename)
    # user_topics = user_topics.loc[user_topics['author'] == "prettyketty88"]
    # lda_model, corpus, dictionary_LDA = get_user_topics("prettyketty88")
    authors = pd.read_csv("preprocessed_documents.csv")
    authors = get_unique_authors(authors)
    authors = filter_authors(authors)
    print(len(authors))
    # print(authors)
    # print("MilosBurrito" in authors)

    # pretty_ketty = pd.read_csv("preprocessed_documents.csv")
    # pretty_ketty = pretty_ketty.loc[pretty_ketty['author'] == "prettyketty88"]
    # print(pretty_ketty)
    # lda_model.top_topics()
    # user_topics = user_topics.loc[user_topics['topic_id'] == 9]
