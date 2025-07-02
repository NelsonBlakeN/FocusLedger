import requests
from datetime import datetime, timedelta

# Fetch project metadata for display names

def fetch_projects(api_token):
    url = "https://api.track.toggl.com/api/v9/me/projects"
    auth = (api_token, "api_token")
    resp = requests.get(url, auth=auth)
    if resp.status_code == 429:
        raise Exception("Toggl API rate limit reached while fetching projects.")
    if resp.status_code == 401:
        raise Exception("Unauthorized: Invalid Toggl API token.")
    if not resp.ok:
        raise Exception(f"Toggl API error: {resp.status_code} {resp.text}")
    return resp.json()
