import os
from itertools import chain  # to flatten list of sentences of tokens into list of tokens
from pprint import pprint

import gensim
import pandas as pd
from gensim import corpora
from gensim import models
from gensim.models import Phrases
from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


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


def get_all_tokens_by_user(df, user):
    all_tokens_by_user = df[df['author'] == user]
    return all_tokens_by_user['tokens'].tolist()


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):  # preprocess_string
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)
    return result


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


if __name__ == "__main__":
    filename = os.path.join("comment_data", "coronavirus_all_comments.csv")
    documents = extract_documents(filename)
    # nltk.download('punkt') # Run only once
    # nltk.download('averaged_perceptron_tagger') # Run only once
    tqdm.pandas()  # Allows progress_map to be used

    # Separates sentences in comment
    documents['sentences'] = documents['body'].progress_map(sent_tokenize)

    # Tokenizes each word in the sentences
    documents['tokens_sentences'] = documents['sentences'].progress_map(
        lambda sentences: [word_tokenize(sentence) for sentence in sentences])

    # Assigns a Part-Of-Speech tag for each token
    documents['POS_tokens'] = documents['tokens_sentences'].progress_map(
        lambda tokens_sentences: [pos_tag(tokens) for tokens in tokens_sentences])

    lemmatizer = WordNetLemmatizer()

    # Lemmatizing each word with its POS tag, in each sentence
    documents['tokens_sentences_lemmatized'] = documents['POS_tokens'].progress_map(
        lambda list_tokens_POS: [
            [
                lemmatizer.lemmatize(el[0], get_wordnet_pos(el[1]))
                if get_wordnet_pos(el[1]) != '' else el[0] for el in tokens_POS
            ]
            for tokens_POS in list_tokens_POS
        ]
    )

    # Flattens sentences array: ['ABC', 'DEF']) --> A B C D E F
    documents['tokens'] = documents['tokens_sentences_lemmatized'].map(
        lambda sentences: list(chain.from_iterable(sentences)))
    documents['tokens'] = documents['tokens'].map(lambda tokens: [token.lower() for token in tokens if token.isalpha()
                                                                  and token.lower() not in
                                                                  stopwords.words('english') and len(token) > 1])

    # get top 10 most frequent names
    n = 10
    authors = documents['author'].value_counts()[:n].index.tolist()
    authors = filter_authors(authors)

    # authors = get_unique_authors(documents)
    print(f"Unique authors: {len(authors)}")

    avg_topic_coherences = []

    for author in authors:
        print(author)
        author_tokens = get_all_tokens_by_user(documents, author)

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
