import ast
import os
from itertools import chain

import pandas as pd
from gensim import corpora
from gensim.models import LdaModel

from definitions import ROOT_DIR
from topic_modelling.user_profile_topic_modelling import get_unique_authors, filter_authors, get_all_tokens_by_user

if __name__ == "__main__":
    lda_file_path = os.path.join("LDA_MODEL", "all_users_lda")
    all_users_lda_model = LdaModel.load(lda_file_path)

    dict_file_path = os.path.join("dictionary_LDA", "all_users_dict")
    all_users_dictionary = corpora.Dictionary.load(dict_file_path)

    # print(all_users_lda_model.show_topic(13))

    documents = pd.read_csv("preprocessed_documents.csv")
    documents["topic"] = ""

    # Each individual comment has their topic predicted
    for index, row in documents.iterrows():
        author_tokens = ast.literal_eval(row["tokens"])
        if len(author_tokens) > 0:  # Do not consider emoticons
            unseen_doc = all_users_dictionary.doc2bow(author_tokens)
            topic_probabilities = all_users_lda_model[unseen_doc]  # (topic_id, contribution)
            # print(topic_probabilities)
            documents.at[index, 'topic'] = max(topic_probabilities, key=lambda item: item[1])
    # print(all_users_lda_model.show_topic(8)) # show a topic given a topic id
    # print(documents.head())
    documents.to_csv("processed_documents.csv", index=False)

    # Author as a whole gets their topic predicted
    df = pd.DataFrame(columns=['author', 'topic'])
    authors = get_unique_authors(documents)
    authors = filter_authors(authors)
    df['author'] = pd.Series(authors)
    for index, row in df.iterrows():
        all_tokens_by_user = documents[documents['author'] == row['author']]
        author_tokens = []
        for _, author_row in all_tokens_by_user.iterrows():
            author_token = ast.literal_eval(author_row['tokens'])
            author_tokens.append(author_token)
        flattened_author_tokens = list(chain.from_iterable(author_tokens))  # flattens token list
        if len(flattened_author_tokens) > 0:  # Do not consider emoticons
            unseen_doc = all_users_dictionary.doc2bow(flattened_author_tokens)
            topic_probabilities = all_users_lda_model[unseen_doc]  # (topic_id, contribution)
            # print(topic_probabilities)
            df.at[index, 'topic'] = max(topic_probabilities, key=lambda item: item[1])
    # print(df.head())

    df.to_csv(os.path.join(ROOT_DIR, "csv_data", "author_topic_association.csv"), index=False)
