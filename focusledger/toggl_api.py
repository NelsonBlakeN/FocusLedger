import requests
from datetime import datetime, timedelta

def fetch_time_entries(api_token, days=7):
    """
    Fetch time entries from Toggl for the last `days` days.
    Returns a list of entries.
    """
    since = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    url = "https://api.track.toggl.com/api/v9/me/time_entries"
    params = {"since": since}
    auth = (api_token, "api_token")
    resp = requests.get(url, params=params, auth=auth)
    if resp.status_code == 401:
        raise Exception("Unauthorized: Invalid Toggl API token.")
    if not resp.ok:
        raise Exception(f"Toggl API error: {resp.status_code} {resp.text}")
    return resp.json()
