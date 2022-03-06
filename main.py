import datetime
import json

import pandas as pd
from pmaw import PushshiftAPI

from data_collection import RedditData


def get_post_ids(files):
    link_IDs = set()
    for file in files:
        f = open(file)
        json_data = json.load(f)
        for submission in json_data:
            if "id" in submission:
                link_IDs.add(submission["id"])
    return link_IDs


def get_submissions_data(data):
    # headers for submissions
    headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
               "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
               "num_crossposts", "over_18", "permalink", "pinned", "post_hint", "preview", "retrieved_on",
               "score", "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers",
               "subreddit_type", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url"]

    # "sort_type = score" provides more results than "sort_type = num_comments"
    reddit_data = data.get_data("submission", "coronavirus", sort_type="score", sort="desc", size=100)
    data.write_data_to_json_file(reddit_data, "submission", "coronavirus")
    data.write_data_to_csv(reddit_data, headers, "submission", "coronavirus")
    return reddit_data


def get_comments_data(data):
    # Cannot sort comments by number of comments (makes sense but documentation is wrong)
    reddit_data = data.get_data("comment", "coronavirus", sort_type="score", sort="desc", size=100)
    # headers = ["author", "author_flair_css_class", "author_flair_text", "body", "created_utc",
    #            "edited", "id", "is_submitter", "link_id", "parent_id", "retrieved_on", "score",
    #            "stickied", "subreddit", "subreddit_id"]
    # data.write_data_to_csv(reddit_data, headers, "comment", "coronavirus")
    return reddit_data


def get_comments_from_submission(subreddit, **kwargs):
    api = PushshiftAPI()

    all_comments = []
    for idx, post_id in enumerate(link_IDs):
        print(f"Query iteration: {idx + 1}")
        comments = api.search_comments(subreddit=subreddit, link_id=post_id, **kwargs)
        comments_list = [comment for comment in comments]
        all_comments.extend(comments_list)

    return all_comments


if __name__ == '__main__':
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())
    data = RedditData(before, after, "test_directory")

    # reddit_submissions = get_submissions_data(data)

    # This line is now redundant due to using PMAW API but kept just in case for testing purposes
    # reddit_comments = get_comments_data(data)

    files = ['./test_directory/coronavirus_submission.json']
    link_IDs = get_post_ids(files)
    print(len(link_IDs))

    all_comments = get_comments_from_submission("coronavirus", sort_type="score", sort="desc")

    headers = ["author", "link_id", "id", "parent_id", "created_utc", "is_submitter", "score", "subreddit",
               "subreddit_id", "body"]

    data.write_data_to_csv(all_comments, headers, "comment", "coronavirus")
