import json
import os


def write_data_to_json_file(data, json_file_path, data_type, subreddit):
    json_file_path = os.path.join(json_file_path, f"{subreddit}_{data_type}.json")
    with open(json_file_path, 'w') as f:
        json.dump(data, f)
