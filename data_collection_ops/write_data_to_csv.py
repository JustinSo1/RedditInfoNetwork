import os

import pandas as pd


def write_data_to_csv(data, headers, file_path, subreddit, data_type):
    csv_file_path = os.path.join(file_path, f"{subreddit}_{data_type}.csv")
    df = pd.DataFrame.from_records(data)[headers]
    df.to_csv(csv_file_path, index=False)
