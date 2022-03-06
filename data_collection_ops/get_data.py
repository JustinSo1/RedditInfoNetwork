import requests


def get_data(time_period, data_type, subreddit, **kwargs):
    before, after = time_period.before, time_period.after
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
