from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer


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


def lemmatize_document(df, column):
    lemmatizer = WordNetLemmatizer()

    # Lemmatizing each word with its POS tag, in each sentence
    return df[column].progress_map(
        lambda list_tokens_POS: [
            [
                lemmatizer.lemmatize(el[0], get_wordnet_pos(el[1]))
                if get_wordnet_pos(el[1]) != '' else el[0] for el in tokens_POS
            ]
            for tokens_POS in list_tokens_POS
        ]
    )
