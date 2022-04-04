from pprint import pprint

from gensim import corpora
from gensim import models
from gensim.models import Phrases
from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS


def topic_modelling(author_tokens):
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
    pprint(top_topics)
    print("------------------------------------------")
    return lda_model, corpus, dictionary_LDA