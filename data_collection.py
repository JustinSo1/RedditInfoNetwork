import collections
import logging

from data_collection_ops.get_data import get_data
from data_collection_ops.write_data_to_csv import write_data_to_csv
from data_collection_ops.write_data_to_json_file import write_data_to_json_file

logger = logging.getLogger(__name__)
TimePeriod = collections.namedtuple("TimePeriod", ["before", "after"])


class RedditData:
    def __init__(self, before=None, after=None, file_path=""):
        logger.info("Hello, world")
        self.time_period = TimePeriod(before, after)
        self.file_path = file_path

    def write_data_to_csv(self, reddit_data, headers, data_type, subreddit):
        try:
            write_data_to_csv(reddit_data, headers, self.file_path, subreddit, data_type)
        except Exception as e:
            logger.exception(e)

    def get_data(self, data_type, subreddit, **kwargs):
        try:
            return get_data(self.time_period, data_type, subreddit, **kwargs)
        except Exception as e:
            logger.exception(e)

    def write_data_to_json_file(self, reddit_data, data_type, subreddit):
        try:
            write_data_to_json_file(reddit_data, self.file_path, data_type, subreddit)
        except Exception as e:
            logger.exception(e)

    def set_time_period(self, before, after):
        self.time_period = TimePeriod(before, after)
