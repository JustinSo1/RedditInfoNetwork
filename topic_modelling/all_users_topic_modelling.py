import os

# LDA model visualization
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

from LDA_topic_modelling import topic_modelling
from data_preprocess_ops.preprocess_documents import preprocess_documents
from user_profile_topic_modelling import extract_documents, filter_authors, \
    get_unique_authors


# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
def get_all_tokens_by_all_users(df, users):
    all_tokens_by_all_users = []

    # Unpack comments into one big list of tokens per user
    for user in users:
        all_tokenized_comments_by_user = df[df['author'] == user]
        all_tokens_by_user = []

        for row in all_tokenized_comments_by_user['tokens']:
            all_tokens_by_user.extend(row)

        all_tokens_by_all_users.append(all_tokens_by_user)

    return all_tokens_by_all_users


if __name__ == "__main__":
    filename = os.path.join("comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)
    # download_nltk_files() # Uncomment when running for the first time

    documents = preprocess_documents(documents)

    # get top 10 most frequent names
    # n = 10
    # authors = get_top_k_frequent_authors(documents, n)
    authors = get_unique_authors(documents)

    authors = filter_authors(authors)

    print(f"Unique authors: {len(authors)}")

    author_tokens = get_all_tokens_by_all_users(documents, authors)

    lda_model, corpus, dictionary_LDA = topic_modelling(author_tokens, num_topics=10, passes=4)

    df = pd.DataFrame(columns=["author", "score", "topic_id", "topic"])
    # Print out topic distribution for each user/document
    for i, doc in enumerate(corpus):
        # print(authors[i])
        for index, score in sorted(lda_model[doc], key=lambda tup: -1 * tup[1]):
            topic = lda_model.print_topic(index, 10)
            # print("Score: {} Topic ID: {} Topic: {}".format(score, index, topic))
            df = df.append(
                {"author": authors[i], "score": score, "topic_id": index, "topic": topic}, ignore_index=True)

    df.to_csv("Topic_Distribution.csv", index=False)
    # Visualize LDA model with pyLDAvis
    vis = gensimvis.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)
    pyLDAvis.save_html(vis, 'all_users_lda.html')
