import os
from pprint import pprint

import pandas as pd
from gensim import corpora
from gensim import models
from gensim.models import Phrases
from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS

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


if __name__ == "__main__":
    filename = os.path.join("comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)

    # download_nltk_files() # Run only once

    documents = preprocess_documents(documents)
    # get top 10 most frequent names
    n = 10
    authors = get_top_k_frequent_authors(documents, n)

    # authors = get_unique_authors(documents)
    print(f"Unique authors: {len(authors)}")

    avg_topic_coherences = []

    for author in authors[1:2]:
        print(author)
        author_tokens = get_all_tokens_by_user(documents, author)

        print(f"Author_tokens: {author_tokens}")

        # Computes Bigram and Trigrams for the tokens
        bigram_model = Phrases(author_tokens, connector_words=ENGLISH_CONNECTOR_WORDS)
        trigram_model = Phrases(bigram_model[author_tokens], min_count=1, connector_words=ENGLISH_CONNECTOR_WORDS)
        author_tokens = list(trigram_model[bigram_model[author_tokens]])

        dictionary_LDA = corpora.Dictionary(author_tokens)
        # dictionary_LDA.filter_extremes(no_below=3)
        corpus = [dictionary_LDA.doc2bow(tok) for tok in author_tokens]

        # print(f"corpus: {corpus}")
        print('Number of unique tokens: %d' % len(dictionary_LDA))
        print('Number of documents: %d' % len(corpus))
        num_topics = 5
        passes = 4
        lda_model = models.LdaModel(corpus, num_topics=num_topics,
                                    id2word=dictionary_LDA,
                                    passes=passes, alpha='auto',
                                    eta='auto', eval_every=False)

        top_topics = lda_model.top_topics(corpus)  # , num_words=20)

        # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
        avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
        print('Average topic coherence: %.4f.' % avg_topic_coherence)
        avg_topic_coherences.append(avg_topic_coherence)
        pprint(top_topics)
        print("------------------------------------------")

    print(avg_topic_coherences)
