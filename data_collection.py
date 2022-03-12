import logging

from data_collection_ops.get_data import get_data
from data_collection_ops.write_data_to_csv import write_data_to_csv
from data_collection_ops.write_data_to_json_file import write_data_to_json_file

logger = logging.getLogger(__name__)


class DataCollection:
    def __init__(self, file_path=""):
        logger.info("Hello, world")
        self.file_path = file_path

    def write_data_to_csv(self, reddit_data, headers, data_type, subreddit):
        logger.info("Writing pushshift data to csv")
        print("Writing pushshift data to csv")

        try:
            write_data_to_csv(reddit_data, headers=headers, file_path=self.file_path, subreddit=subreddit,
                              data_type=data_type)
        except Exception as e:
            logger.exception(e)

    def get_data(self, data_type, subreddit, **kwargs):
        logger.info("Getting pushshift data")
        print("Getting pushshift data")

        try:
            return get_data(data_type, subreddit, **kwargs)
        except Exception as e:
            logger.exception(e)

    def write_data_to_json_file(self, reddit_data, data_type, subreddit):
        logger.info("Writing pushshift data to json")
        print("Writing pushshift data to json")

        try:
            write_data_to_json_file(reddit_data, self.file_path, data_type, subreddit)
        except Exception as e:
            logger.exception(e)
