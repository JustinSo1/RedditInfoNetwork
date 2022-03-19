import os

import pandas as pd


def write_data_to_csv(data, headers, file_path, subreddit, data_type):
    csv_file_path = os.path.join(file_path, f"{subreddit}_{data_type}.csv")
<<<<<<< HEAD
    df = pd.DataFrame.from_records(data)[headers]
    df.to_csv(csv_file_path, index=False)
=======
    if headers:
        df = pd.DataFrame.from_records(data)[headers]
        df.to_csv(csv_file_path, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, header=True, index=False, columns=list(df.axes[1]))
>>>>>>> dadaf2997fced4354a039c47d28080cde2b2d6eb
