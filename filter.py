import json
import os
import requests
import datetime
import pandas as pd

# # json format
# [
#  {...}, ..., {...}
# ]


def convert_comment_data_to_csv(subreddit, before, after, link_id):
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
        link_id=link_id
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
            link_id=link_id
        ).get("data")

        all_results.extend(results)
        query_iteration += 1
        print("Query iteration: {}".format(query_iteration))

    for comment in all_results:
        all_comments.append(comment)


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
    print(request.status_code)
    return request.json()


def write_comments_to_json_file(subreddit, data):
    json_file_path = os.path.join("comment_data", f"{subreddit}_all_comments.json")
    with open(json_file_path, 'w') as f:
        json.dump(data, f)


subreddits = ["coronavirus", "news", "politics", "ideological", "local", "science", "technology", "health", "business"]

files = ['./submission_data/coronavirus_submissions.json']

link_id = set()
all_comments = []

for file in files:
    f = open(file)
    data = json.load(f)
    for i in data:
        # get all link_ids/ post ids
        # get link id from post
        if "id" in i:
            link_id.add(i["id"])

print(link_id)
before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())

l = 1
for id in link_id:
    if l <= 15: # arbitary number/ top 15 posts sorted by score (want to change to # of comments)
        print("{}: Getting comments for post {}".format(l, id))
        convert_comment_data_to_csv(subreddit="coronavirus",
                                    before=before,
                                    after=after,
                                    link_id=id)
    l += 1

write_comments_to_json_file("coronavirus", all_comments)
# Select the columns you care about
headers = ["author", "body", "created_utc", "edited", "id", "is_submitter", "link_id", "parent_id",
           "retrieved_on", "score", "stickied", "subreddit", "subreddit_id"]

df = pd.DataFrame.from_records(all_comments)[headers]
# ..._all_comments holds comments from top 15 posts
# ..._comments
csv_file_path = os.path.join("comment_data", "coronavirus_all_comments.csv")
df.to_csv(csv_file_path, index=False)
