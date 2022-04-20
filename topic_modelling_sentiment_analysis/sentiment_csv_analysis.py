import os

import pandas as pd

from definitions import ROOT_DIR

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(ROOT_DIR, "csv_data", "author_common_topic_pairs.csv"))
