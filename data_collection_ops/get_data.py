<<<<<<< HEAD
import requests


def get_data(time_period, data_type, subreddit, **kwargs):
    before, after = time_period.before, time_period.after

    # Quick fix for getting comments since date doesn't matter
    if not before and not after:
        return get_pushshift_data(data_type, subreddit=subreddit, **kwargs)

    all_results = results = get_pushshift_data(
        before=before,
        after=after,
        data_type=data_type,
        subreddit=subreddit,
        **kwargs
    ).get("data")
    query_iteration = 1
    while len(results) != 0:
        print("Query iteration: {}".format(query_iteration))
        after_new = results[-1]["created_utc"]
        results = get_pushshift_data(
            after=after_new,
            before=before,
            data_type=data_type,
            subreddit=subreddit,
            **kwargs
        ).get("data")

        all_results.extend(results)
        query_iteration += 1

    return all_results


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
=======
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
>>>>>>> dadaf2997fced4354a039c47d28080cde2b2d6eb
