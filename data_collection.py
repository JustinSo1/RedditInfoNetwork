import collections
import logging
import datetime

from data_collection_ops.get_data import get_data
from data_collection_ops.write_data_to_csv import write_data_to_csv
from data_collection_ops.write_data_to_json_file import write_data_to_json_file

logger = logging.getLogger(__name__)


class RedditData:
    def __init__(self, before=None, after=None, file_path=""):
        logger.info("Hello, world")
        TimePeriod = collections.namedtuple("TimePeriod", ["before", "after"])
        self.time_period = TimePeriod(before, after)
        self.file_path = file_path

    def write_data_to_csv(self, reddit_data, headers, data_type, subreddit):
        try:
            write_data_to_csv(reddit_data, headers, self.file_path, subreddit, data_type)
        except Exception as e:
            logger.exception(e)

    def get_data(self, data_type, subreddit, **kwargs):
        try:
            reddit_data = get_data(self.time_period, data_type, subreddit, **kwargs)
            return reddit_data
            # if not reddit_data["error_message"]:
            #     print("Gratz")
            # else:
            #     print(reddit_data["error_message"])
        except Exception as e:
            logger.exception(e)

    def write_data_to_json_file(self, reddit_data, data_type, subreddit):
        try:
            write_data_to_json_file(reddit_data, self.file_path, data_type, subreddit)
        except Exception as e:
            logger.exception(e)


# import logging
#
#
# def main():
#     logging.basicConfig(filename='myapp.log', level=logging.INFO)
#     logging.info('Started')
#
#     logging.info('Finished')
#
#
if __name__ == '__main__':
    before = int(datetime.datetime(year=2020, month=12, day=31).timestamp())
    after = int(datetime.datetime(year=2020, month=1, day=1).timestamp())
    data = RedditData(before, after, "test_directory")
    reddit_data = data.get_data("submission", "coronavirus", sort_type="num_comments", sort="desc", size=100)
    headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
               "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
               "num_crossposts", "over_18", "permalink", "pinned", "post_hint", "preview", "retrieved_on",
               "score", "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers",
               "subreddit_type", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url"]
    data.write_data_to_csv(reddit_data, headers, "submission", "coronavirus")
    # data.convert_data_to_csv("", "", "")

# main()
