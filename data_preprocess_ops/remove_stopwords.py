from nltk.corpus import stopwords


def remove_stopwords(df, column):
    return df[column].map(lambda tokens: [token.lower() for token in tokens if token.isalpha()
                                          and token.lower() not in
                                          stopwords.words('english') and len(token) > 1])
