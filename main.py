import os
import datetime

import pandas as pd
import requests
import json


def convert_submission_data_to_csv(subreddit, before, after):
    data_type = "submission"  # give me comments, use "submission" to publish something
    sort_type = "score"  # Sort by score (Accepted: "score", "num_comments", "created_utc")
    sort = "desc"  # sort descending
    size = 100  # number of results to return

    query_iteration = 1

    all_results = results = get_pushshift_data(
        data_type=data_type,
        # q=query,
        after=after,
        before=before,
        size=size,
        sort_type=sort_type,
        sort=sort,
        subreddit=subreddit,
        ).get("data")
    
    while len(results) != 0:
        after_new = results[-1]["created_utc"]
        results = get_pushshift_data(
            data_type=data_type,
            # q=query,
            after=after_new,
            before=before,
            size=size,
            sort_type=sort_type,
            sort=sort,
            subreddit=subreddit,
            ).get("data")
        
        all_results.extend(results)
        query_iteration += 1
        print("Query iteration: {}".format(query_iteration))

    data = all_results

    write_submissions_to_json_file(subreddit, data)
    # Select the columns you care about
    headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
               "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
               "num_crossposts", "over_18", "permalink", "pinned", "post_hint", "preview", "retrieved_on", 
               "score", "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers", 
               "subreddit_type", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url", ]

    df = pd.DataFrame.from_records(data)[headers]

    df['selftext'] = df['selftext'].replace(r'\n', ' ', regex=True)

    # Append the string to all the permalink entries so that we have a link to the comment
    df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)

    df.style.format({'permalink': make_clickable})

    csv_file_path = os.path.join("submission_data", f"{subreddit}_submissions.csv")
    df.to_csv(csv_file_path, index=False)

def convert_comment_data_to_csv(subreddit, before, after):
    data_type = "comment"  # give me comments, use "submission" to publish something
    sort_type = "score"  # Sort by score (Accepted: "score", "num_comments", "created_utc")
    sort = "desc"  # sort descending
    size = 100  # number of results to return
    
    query_iteration = 1

    all_results = results = get_pushshift_data(
        data_type=data_type,
        # q=query,
        after=after,
        before=before,
        size=size,
        sort_type=sort_type,
        sort=sort,
        subreddit=subreddit,
        ).get("data")
    
    while len(results) != 0:
        after_new = results[-1]["created_utc"]
        results = get_pushshift_data(
            data_type=data_type,
            # q=query,
            after=after_new,
            before=before,
            size=size,
            sort_type=sort_type,
            sort=sort,
            subreddit=subreddit,
            ).get("data")
        
        all_results.extend(results)
        query_iteration += 1
        print("Query iteration: {}".format(query_iteration))

    data = all_results

    write_comments_to_json_file(subreddit, data)
    # Select the columns you care about
    headers = ["author", "author_flair_css_class", "author_flair_text", "body", "created_utc",
               "edited", "id", "is_submitter", "link_id", "parent_id", "retrieved_on", "score",
               "stickied", "subreddit", "subreddit_id"]

    df = pd.DataFrame.from_records(data)[headers]

    csv_file_path = os.path.join("comment_data", f"{subreddit}_comments.csv")
    df.to_csv(csv_file_path, index=False)


def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.

    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.

    Read more: https://github.com/pushshift/api
    """

    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()


def write_submissions_to_json_file(subreddit, data):
    json_file_path = os.path.join("submission_data", f"{subreddit}_submissions.json")
    with open(json_file_path, 'w') as f:
        json.dump(data, f)

def write_comments_to_json_file(subreddit, data):
    json_file_path = os.path.join("comment_data", f"{subreddit}_comments.json")
    with open(json_file_path, 'w') as f:
        json.dump(data, f)


# Create a function to make the link clickable and style the last column
def make_clickable(val):
    """ Makes a pandas column clickable by wrapping it in some html.
    """
    return '<a href="{}">Link</a>'.format(val, val)


if __name__ == "__main__":
    # https://api.pushshift.io/reddit/search/comment/?q=trump&after=4d&before=2d&sort=asc
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())
    # print(before, after)
    # print("Start getting post data")
    # with open("subreddit_list.txt") as subreddit_list:
    #     while subreddit := subreddit_list.readline():
    #         print(f"Getting post data for {subreddit}")
    #         convert_submission_data_to_csv(subreddit.rstrip(),
    #                                        before=before,
    #                                        after=after)
    # print("Finished getting post data")
    print("Start getting comment data")
    with open("subreddit_list.txt") as subreddit_list:
        while subreddit := subreddit_list.readline():
            print(f"Getting comment data for {subreddit}")
            convert_comment_data_to_csv(subreddit.rstrip(),
                                        before=before,
                                        after=after)
    print("Finished getting comment data")
