from pmaw import PushshiftAPI


def get_data(data_type, subreddit, **kwargs):
    api = PushshiftAPI()
    func_mapping = {
        "comment": get_pushshift_comments,
        "submission": get_pushshift_submissions
    }
    pushshift_data = func_mapping[data_type](api, subreddit, **kwargs)

    return pushshift_data


def get_pushshift_comments(api, subreddit, **kwargs):
    """
    Gets data from the pushshift api.
    Read more: https://github.com/pushshift/api
    """
    return api.search_comments(subreddit=subreddit, **kwargs)


def get_pushshift_submissions(api, subreddit, **kwargs):
    """
    Gets data from the pushshift api.
    Read more: https://github.com/pushshift/api
    """
    return api.search_submissions(subreddit=subreddit, **kwargs)
