import requests
from datetime import datetime, timedelta

def fetch_time_entries(api_token, days=7):
    """
    Fetch time entries from Toggl for the last `days` days.
    Returns a list of entries.
    Raises RateLimitError if rate limit is reached.
    """
    # Toggl API v9 expects 'since' as a unix timestamp (integer)
    since_dt = datetime.utcnow() - timedelta(days=days)
    since = int(since_dt.timestamp())
    url = "https://api.track.toggl.com/api/v9/me/time_entries"
    params = {"since": since}
    auth = (api_token, "api_token")
    resp = requests.get(url, params=params, auth=auth)
    if resp.status_code == 429:
        raise RateLimitError("Toggl API rate limit reached. Displaying partial data.")
    if resp.status_code == 401:
        raise Exception("Unauthorized: Invalid Toggl API token.")
    if not resp.ok:
        raise Exception(f"Toggl API error: {resp.status_code} {resp.text}")
    return resp.json()


# Custom exception for rate limiting
class RateLimitError(Exception):
    pass
