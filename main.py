import datetime

from data_collection import DataCollection

if __name__ == '__main__':
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())
    directory = "test_directory"
    data = DataCollection(directory)
    with open("subreddit_list.txt") as file:
        while subreddit := file.readline():
            stripped_subreddit = subreddit.rstrip()
            headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
                       "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
                       "num_crossposts", "over_18", "permalink", "pinned", "post_hint", "preview", "retrieved_on",
                       "score", "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers",
                       "subreddit_type", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url"]

            reddit_submissions = data.get_data(subreddit=stripped_subreddit, data_type="submission", sort_type="score",
                                               sort="desc",
                                               before=before, after=after)
            submission_list = [submission for submission in reddit_submissions]
            print(f"{len(submission_list)} submissions retrieved")

            data.write_data_to_csv(reddit_data=submission_list, headers=headers, data_type="submission",
                                   subreddit=stripped_subreddit)

            reddit_comments = data.get_data(subreddit=stripped_subreddit, data_type="comment", before=before,
                                            after=after,
                                            sort_type="score", sort="desc")
            comments_list = [comment for comment in reddit_comments]
            print(f"{len(comments_list)} comments retrieved")

            data.write_data_to_csv(reddit_data=comments_list, headers=[], data_type="comment",
                                   subreddit=stripped_subreddit)
