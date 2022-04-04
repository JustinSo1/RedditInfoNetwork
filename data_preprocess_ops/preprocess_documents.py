from itertools import chain

from tqdm import tqdm
from data_preprocess_ops.add_POS_tag import add_POS_tag
from data_preprocess_ops.lemmatize_document import lemmatize_document
from data_preprocess_ops.remove_stopwords import remove_stopwords
from data_preprocess_ops.tokenize_document import tokenize_sentence, tokenize_comment


def preprocess_documents(documents):
    """
    documents: Dataframe
    Creates new columns of each step and final result will be in 'tokens' column
    """
    tqdm.pandas()  # Allows progress_map to be used

    # Separates sentences in comment
    documents['sentences'] = tokenize_sentence(documents, 'body')

    # Tokenizes each word in the sentences
    documents['tokens_sentences'] = tokenize_comment(documents, 'sentences')

    # Assigns a Part-Of-Speech tag for each token
    documents['POS_tokens'] = add_POS_tag(documents, 'tokens_sentences')

    # Lemmatizing each word with its POS tag, in each sentence
    documents['tokens_sentences_lemmatized'] = lemmatize_document(documents, 'POS_tokens')

    # Flattens sentences array: ['ABC', 'DEF']) --> A B C D E F
    documents['tokens'] = documents['tokens_sentences_lemmatized'].map(
        lambda sentences: list(chain.from_iterable(sentences)))
    documents['tokens'] = remove_stopwords(documents, 'tokens')

    return documents
