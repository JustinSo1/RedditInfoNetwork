import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pandas as pd


def get_sentiment(text, analyzer):
    """
    positive sentiment: compound score >= 0.05
    neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    negative sentiment: compound score <= -0.05
    """
    threshold = 0.05
    vs = analyzer.polarity_scores(text)
    compound_score = vs['compound']
    if compound_score >= threshold:
        return "pos", compound_score
    elif -threshold < compound_score < threshold:
        return "neu", compound_score
    else:  # <= -threshold
        return "neg", compound_score


if __name__ == "__main__":
    filename = os.path.join("processed_documents.csv")
    data = pd.read_csv(filename)
    analyzer = SentimentIntensityAnalyzer()
    # TODO: update this to match data in new csv
    # sentiment: {sentiment_polarity, sentiment_score}
    data['sentiment'] = data.apply(lambda row: get_sentiment(row['body'], analyzer), axis=1)
    data.to_csv(filename, index=False)
    print(data)
