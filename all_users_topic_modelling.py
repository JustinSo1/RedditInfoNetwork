import os

# LDA model visualization
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

from LDA_topic_modelling import topic_modelling
from data_preprocess_ops.filter_comments import filter_comments
from data_preprocess_ops.preprocess_documents import preprocess_documents
from user_profile_topic_modelling import extract_documents, get_top_k_frequent_authors, filter_authors


# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
def get_all_tokens_by_all_users(df, users):
    all_tokens_by_all_users = []

    # Unpack comments into one big list of tokens per user
    for user in users:
        all_tokenized_comments_by_user = df[df['author'] == user]
        all_tokens_by_user = []

        for row in all_tokenized_comments_by_user['tokens']:
            all_tokens_by_user += row

        all_tokens_by_all_users.append(all_tokens_by_user)

    return all_tokens_by_all_users


if __name__ == "__main__":
    filename = os.path.join("comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)
    # download_nltk_files() # Uncomment when running for the first time

    ignored_text = ["Your post or comment has been removed", "Microsoft SQL server"]
    documents = filter_comments(documents, 'body', ignored_text)

    documents = preprocess_documents(documents)

    # get top 10 most frequent names
    n = 10
    authors = get_top_k_frequent_authors(documents, n)

    authors = filter_authors(authors)

    print(f"Unique authors: {len(authors)}")

    author_tokens = get_all_tokens_by_all_users(documents, authors)

    lda_model, corpus, dictionary_LDA = topic_modelling(author_tokens)

    # Print out topic distribution for each user/document
    for i, doc in enumerate(corpus):
        print(authors[i])
        for index, score in sorted(lda_model[doc], key=lambda tup: -1 * tup[1]):
            print("Score: {}\t Topic ID: {} Topic: {}".format(score, index, lda_model.print_topic(index, 10)))

    # Visualize LDA model with pyLDAvis
    vis = gensimvis.prepare(topic_model=lda_model, corpus=corpus, dictionary=dictionary_LDA)
    pyLDAvis.save_html(vis, 'all_users_lda.html')
