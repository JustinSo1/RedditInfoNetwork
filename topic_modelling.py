import os
from pprint import pprint

import gensim
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS
from nltk.stem.wordnet import WordNetLemmatizer


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


def get_all_comments_by_user(df, user):
    all_comments_by_author = df[df['author'] == user]
    return all_comments_by_author['body'].tolist()


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):  # preprocess_string
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)
    return result


if __name__ == "__main__":

    filename = os.path.join("comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)
    # get top 10 most frequent names
    n = 10
    authors = documents['author'].value_counts()[:n].index.tolist()
    authors = filter_authors(authors)
    # authors = get_unique_authors(documents)
    # print(f"Unique authors: {len(authors)}")
    # most_frequent_authors = get_top_k_frequent_authors(documents, n)
    # print(most_frequent_authors)

    avg_topic_coherences = []

    for author in authors:
        print(author)
        docs = get_all_comments_by_user(documents, author)
        if len(docs) < 10:  # Get rid of users with less than 10 comments
            continue
        print(f"Amount of comments: {len(docs)}")
        print(f"Sentence: {docs}")
        docs = [preprocess(doc) for doc in docs]
        print(f"preprocess: {docs}")

        lemmatizer = WordNetLemmatizer()
        docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]

        print(f"lemmatized: {docs}")

        # Add bigrams and trigrams to docs (only ones that appear 20 times or more).
        bigram = Phrases(docs, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
        for idx in range(len(docs)):
            for token in bigram[docs[idx]]:
                if '_' in token:
                    # Token is a bigram, add to document.
                    docs[idx].append(token)
        print(f"bigrams: {docs}")
        # Remove rare and common tokens.
        # Create a dictionary representation of the documents.
        dictionary = Dictionary(docs)

        # Bag-of-words representation of the documents.
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        print(f"corpus: {corpus}")
        print('Number of unique tokens: %d' % len(dictionary))
        print('Number of documents: %d' % len(corpus))

        # Train LDA model.
        # Set training parameters.
        num_topics = 5
        chunksize = 2000
        passes = 20
        iterations = 400
        eval_every = None  # Don't evaluate model perplexity, takes too much time.

        # Make a index to word dictionary.
        temp = dictionary[0]  # This is only to "load" the dictionary.
        id2word = dictionary.id2token

        model = LdaModel(
            corpus=corpus,
            id2word=id2word,
            chunksize=chunksize,
            alpha='auto',
            eta='auto',
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=eval_every
        )

        top_topics = model.top_topics(corpus)  # , num_words=20)

        # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
        avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
        print('Average topic coherence: %.4f.' % avg_topic_coherence)
        avg_topic_coherences.append(avg_topic_coherence)
        pprint(top_topics)
        print("------------------------------------------")

    print(avg_topic_coherences)
