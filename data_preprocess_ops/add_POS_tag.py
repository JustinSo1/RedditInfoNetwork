from nltk import pos_tag


def add_POS_tag(df, column):
    return df[column].progress_map(
        lambda tokens_sentences: [pos_tag(tokens) for tokens in tokens_sentences])
