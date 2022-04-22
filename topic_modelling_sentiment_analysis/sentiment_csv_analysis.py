import os
import collections
import pandas as pd

from definitions import ROOT_DIR

def get_topic_sentiment_stats(df):
    # {'topic': {'pos_pos', 'neg_neg', 'neu_neu', 'pos_neg', 'pos_neu', 'neg_neu', 'total'}}
    topic_sentiment_stats_dict = collections.defaultdict(lambda: collections.defaultdict(int))
    for index, row in df.iterrows():
        topic = row['common_topic']
        sentiments = str(row['sentiment1'] + '_' + row['sentiment2'])
        if sentiments == 'neg_pos':
            sentiments = 'pos_neg'
        elif sentiments == 'neu_pos':
            sentiments = 'pos_neu'
        elif sentiments == 'neu_neg':
            sentiments = 'neg_neu'
        topic_sentiment_stats_dict[topic][sentiments] += 1
        topic_sentiment_stats_dict[topic]["total"] += 1

    topics = list(topic_sentiment_stats_dict.keys())
    # sentiments
    totals = [x["total"] for x in list(topic_sentiment_stats_dict.values())]
    pos_pos = [x["pos_pos"] for x in list(topic_sentiment_stats_dict.values())]
    neu_neu = [x["neu_neu"] for x in list(topic_sentiment_stats_dict.values())]
    neg_neg = [x["neg_neg"] for x in list(topic_sentiment_stats_dict.values())]
    pos_neg = [x["pos_neg"] for x in list(topic_sentiment_stats_dict.values())]
    pos_neu = [x["pos_neu"] for x in list(topic_sentiment_stats_dict.values())]
    neg_neu = [x["neg_neu"] for x in list(topic_sentiment_stats_dict.values())]

    # take average
    avg_pos_pos = []
    avg_neu_neu = []
    avg_neg_neg = []
    avg_pos_neg = []
    avg_pos_neu = []
    avg_neg_neu = []
    for i, tot in enumerate(totals):
        avg_pos_pos.append(round(pos_pos[i]/tot*100, 2))
        avg_neu_neu.append(round(neu_neu[i]/tot*100, 2))
        avg_neg_neg.append(round(neg_neg[i]/tot*100, 2))
        avg_pos_neg.append(round(pos_neg[i]/tot*100, 2))
        avg_pos_neu.append(round(pos_neu[i]/tot*100, 2))
        avg_neg_neu.append(round(neg_neu[i]/tot*100, 2))

    # create dataframe
    topic_sentiment_stats_data = {'topic':topics, 'pos_pos':pos_pos, 'neg_neg':neg_neg, 'neu_neu':neu_neu, 'pos_neg':pos_neg, 'pos_neu':pos_neu, 'neg_neu':neg_neu, 'total':totals, 'avg_pos_pos':avg_pos_pos, 'avg_neg_neg':avg_neg_neg, 'avg_neu_neu':avg_neu_neu, 'avg_pos_neg':avg_pos_neg, 'avg_pos_neu':avg_pos_neu, 'avg_neg_neu':avg_neg_neu}

    topic_sentiment_stats_df = pd.DataFrame(topic_sentiment_stats_data)
    
    return topic_sentiment_stats_df

def get_author_pairs_sentiment_stats(df, author):
    # for a particular user's topic participation, get number of same vs. different sentiments in author pairs
    # {'user': {'topic', 'pos_pos', 'neg_neg', 'neu_neu', 'pos_neg', 'pos_neu', 'neg_neu', 'total'}}

    author_pairs_sentiment_stats_dict = collections.defaultdict(lambda: collections.defaultdict(int))
    author_df = df.loc[df['author1'] == author]    
    
    for index, row in author_df.iterrows():
        author = row['author1']
        topic = row['common_topic']
        sentiments = str(row['sentiment1'] + '_' + row['sentiment2'])
        if sentiments == 'neg_pos':
            sentiments = 'pos_neg'
        elif sentiments == 'neu_pos':
            sentiments = 'pos_neu'
        elif sentiments == 'neu_neg':
            sentiments = 'neg_neu'
        
        author_pairs_sentiment_stats_dict[topic][sentiments] += 1
        author_pairs_sentiment_stats_dict[topic]["total"] += 1

    topics = list(author_pairs_sentiment_stats_dict.keys())
    # sentiments
    totals = [x["total"] for x in list(author_pairs_sentiment_stats_dict.values())]
    pos_pos = [x["pos_pos"] for x in list(author_pairs_sentiment_stats_dict.values())]
    neu_neu = [x["neu_neu"] for x in list(author_pairs_sentiment_stats_dict.values())]
    neg_neg = [x["neg_neg"] for x in list(author_pairs_sentiment_stats_dict.values())]
    pos_neg = [x["pos_neg"] for x in list(author_pairs_sentiment_stats_dict.values())]
    pos_neu = [x["pos_neu"] for x in list(author_pairs_sentiment_stats_dict.values())]
    neg_neu = [x["neg_neu"] for x in list(author_pairs_sentiment_stats_dict.values())]

    # take average
    avg_pos_pos = []
    avg_neu_neu = []
    avg_neg_neg = []
    avg_pos_neg = []
    avg_pos_neu = []
    avg_neg_neu = []
    for i, tot in enumerate(totals):
        avg_pos_pos.append(round(pos_pos[i]/tot*100, 2))
        avg_neu_neu.append(round(neu_neu[i]/tot*100, 2))
        avg_neg_neg.append(round(neg_neg[i]/tot*100, 2))
        avg_pos_neg.append(round(pos_neg[i]/tot*100, 2))
        avg_pos_neu.append(round(pos_neu[i]/tot*100, 2))
        avg_neg_neu.append(round(neg_neu[i]/tot*100, 2))

    # create dataframe
    author_pairs_sentiment_stats_data = {'topic':topics, 'pos_pos':pos_pos, 'neg_neg':neg_neg, 'neu_neu':neu_neu, 'pos_neg':pos_neg, 'pos_neu':pos_neu, 'neg_neu':neg_neu, 'total':totals, 'avg_pos_pos':avg_pos_pos, 'avg_neg_neg':avg_neg_neg, 'avg_neu_neu':avg_neu_neu, 'avg_pos_neg':avg_pos_neg, 'avg_pos_neu':avg_pos_neu, 'avg_neg_neu':avg_neg_neu}

    author_pairs_sentiment_stats_df = pd.DataFrame(author_pairs_sentiment_stats_data)

    return author_pairs_sentiment_stats_df

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(ROOT_DIR, "csv_data", "author_common_topic_pairs.csv"))
    
    # write topic_sentiment_stats dataframe to csv file
    csv_folder = "csv_data"
    topic_sentiment_stats_df = get_topic_sentiment_stats(df)
    topic_sentiment_stats_df.to_csv(os.path.join(ROOT_DIR, csv_folder, "topic_sentiment_stats.csv"), index=False)

    # for top 10 authors (based on degree centrality), write author_pairs_sentiment_stats dataframe to csv file
    individual_author_csv_folder = "csv_data/individual_author_topic_sentiment_stats"
    authors = df['author1'].unique()
    for author in authors[:10]:
        author_pairs_sentiment_stats_df = get_author_pairs_sentiment_stats(df, author)
        author_pairs_sentiment_stats_df.to_csv(os.path.join(ROOT_DIR, individual_author_csv_folder, (author + "_author_pairs_sentiment_stats_df.csv")), index=False)