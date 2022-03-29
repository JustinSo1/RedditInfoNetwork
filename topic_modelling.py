import logging
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
    coc_path = os.path.join("comment_data", filename)
    comments_df = pd.read_csv(coc_path)
    comments_df = comments_df[['author', 'body']]
    comments_df = comments_df.sort_values(by=['author'], ascending=True)
    return comments_df


def get_all_comments_by_user(user):
    all_comments_by_author = docs[docs['author'] == user]
    return all_comments_by_author['body'].tolist()


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):  # preprocess_string
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)
    return result


if __name__ == "__main__":

    docs = extract_documents("coronavirus_all_comments.csv")
    # get top 10 most frequent names
    n = 10
    most_frequent_names = docs['author'].value_counts()[:n].index.tolist()
    print(most_frequent_names)

    docs = get_all_comments_by_user(most_frequent_names[2])

    print(f"Sentence: {docs}")
    print(f"L: {len(docs)}")

    docs = [preprocess(doc) for doc in docs]
    print(f"preprocessed = {docs}")

    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]

    print(f"lemmatized = {docs}")

    # Add bigrams and trigrams to docs (only ones that appear 20 times or more).
    bigram = Phrases(docs, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    print(f"bigrams = {docs}")

    # Remove rare and common tokens.
    # Create a dictionary representation of the documents.
    dictionary = Dictionary(docs)
    print(dictionary)

    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    print(corpus)
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

    pprint(top_topics)
