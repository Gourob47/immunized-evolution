def backoff_seconds(attempt):
    # Bug: linear backoff and no negative guard
    return attempt
