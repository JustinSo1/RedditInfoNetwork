import ast

import pandas as pd

from topic_modelling.user_profile_topic_modelling import get_comment_topic


def get_unique_authors(df):
    return df["author"].unique()


if __name__ == "__main__":
    # filename = os.path.join("Topic_Distribution.csv")
    documents = pd.read_csv("preprocessed_documents.csv")
    documents["topics"] = ""
    documents = documents.reset_index()  # make sure indexes pair with number of rows
    documents = documents.drop(labels='index', axis=1)
    for index, row in documents.iterrows():
        # print(row)
        row_tokens = ast.literal_eval(row["tokens"])
        if len(row_tokens) > 0:  # Do not consider emoticons
            lda_model, corpus, dictionary_LDA = get_comment_topic([row_tokens])
            documents.at[index, 'topics'] = lda_model.top_topics(corpus)
    # print(documents.head())
    documents.to_csv("processed_documents.csv", index=False)
