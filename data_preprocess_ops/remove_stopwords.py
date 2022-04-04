from nltk.corpus import stopwords

stopwords = stopwords.words('english') + ['https', 'http']


def remove_stopwords(df, column):
    return df[column].map(lambda tokens: [token.lower() for token in tokens if token.isalpha()
                                          and token.lower() not in
                                          stopwords and len(token) > 1])
