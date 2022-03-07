import datetime
import json

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


def get_comments_from_submission(api, link_IDs, subreddit, **kwargs):
    all_comments = []
    for idx, post_id in enumerate(link_IDs):
        print(f"Query iteration: {idx + 1}")
        comments = api.get_data(data_type="comment", subreddit=subreddit, link_id=post_id, **kwargs)
        comments_list = [comment for comment in comments]
        all_comments.extend(comments_list)

    return all_comments


if __name__ == '__main__':
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=0).timestamp())
    directory = "test_directory"
    data = RedditData("test_directory")

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
    # data.write_data_to_json_file(reddit_data, "submission", "coronavirus")

    # files = ['./test_directory/coronavirus_submission.json']
    # link_IDs = get_post_ids(files)
    # # print(len(link_IDs))
    #
    # all_comments = get_comments_from_submission(api=data, link_IDs=link_IDs, subreddit="coronavirus", sort_type="score",
    #                                             sort="desc")
    # headers = ["author", "link_id", "id", "parent_id", "created_utc", "is_submitter", "score", "subreddit",
    #            "subreddit_id", "body"]
    #
    # data.write_data_to_csv(all_comments, headers, "comment", "coronavirus")
