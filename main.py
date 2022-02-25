import pandas as pd
import requests


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


if __name__ == "__main__":
    # https://api.pushshift.io/reddit/search/comment/?q=trump&after=4d&before=2d&sort=asc

    data_type = "submission"  # give me comments, use "submission" to publish something
    query = "python"  # Add your query
    duration = "30d"  # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
    size = 10  # maximum 1000 comments
    sort_type = "score"  # Sort by score (Accepted: "score", "num_comments", "created_utc")
    sort = "desc"  # sort descending
    aggs = "subreddit"  # "author", "link_id", "created_utc", "subreddit"

    # Call the API
    data = get_pushshift_data(data_type=data_type,
                              q=query,
                              after="4d",
                              before="2d",
                              size=size,
                              sort_type=sort_type,
                              sort=sort).get("data")

    # Select the columns you care about
    # headers = ["author", "created_utc", "awarders", "domain", "full_link", "gildings", "id", "is_crosspostable",
    #            "is_original_content", "is_reddit_media_domain", "is_self", "is_video", "locked", "num_comments",
    #            "num_crossposts", "over_18", "permalink", "pinned", "removed_by_category", "retrieved_on", "score",
    #            "selftext", "stickied", "subreddit", "subreddit_id", "subreddit_subscribers", "subreddit_type",
    #            "suggested_sort", "thumbnail", "title", "total_awards_received", "upvote_ratio", "url", "post_hint",
    #            "preview", "banned_by", "edited", "html_decode"]
    # df = pd.DataFrame.from_records(data)[headers]
    #
    # # Keep the first 400 characters
    # df['selftext'] = df['selftext'].str[0:400] + "..."
    # df['selftext'] = df['selftext'].replace(r'\n', ' ', regex=True)
    #
    # # Append the string to all the permalink entries so that we have a link to the comment
    # df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)
    #
    #
    # # Create a function to make the link to be clickable and style the last column
    # def make_clickable(val):
    #     """ Makes a pandas column clickable by wrapping it in some html.
    #     """
    #     return '<a href="{}">Link</a>'.format(val, val)
    #
    #
    # df.style.format({'permalink': make_clickable})
    # df.to_csv('file_name.csv', index=False)
