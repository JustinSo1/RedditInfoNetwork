from nltk.tokenize import sent_tokenize, word_tokenize


def tokenize_comment(df, column):
    return df[column].progress_map(
        lambda sentences: [word_tokenize(sentence) for sentence in sentences])


def tokenize_sentence(df, column):
    return df[column].progress_map(sent_tokenize)
