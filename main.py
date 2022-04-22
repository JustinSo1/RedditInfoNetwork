import datetime
import os

import pandas as pd

from data_collection.data_collection import DataCollection
from definitions import ROOT_DIR

if __name__ == '__main__':
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())
    directory = os.path.join(ROOT_DIR)
    data = DataCollection(directory)
    headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
               "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
               "num_crossposts", "over_18", "permalink", "pinned", "post_hint", "preview", "retrieved_on",
               "score", "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers",
               "subreddit_type", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url"]
    reddit_submissions = data.get_data(subreddit="coronavirus", data_type="submission", sort_type="score", sort="desc",
                                       before=before, after=after)
    submission_list = [submission for submission in reddit_submissions]
    print(f"{len(submission_list)} submissions retrieved")

    data.write_data_to_csv(submission_list, headers, "submission", "coronavirus")

    reddit_comments = data.get_data(subreddit="coronavirus", data_type="comment", before=before, after=after,
                                    sort_type="score", sort="desc")
    comments_list = [comment for comment in reddit_comments]
    print(f"{len(comments_list)} comments retrieved")

    comments_df = pd.DataFrame(comments_list)

    comments_df.to_csv(ROOT_DIR + "/data_collection/coronavirus_comments.csv", header=True, index=False, columns=list(comments_df.axes[1]))
