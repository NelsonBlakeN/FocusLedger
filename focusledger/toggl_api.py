import requests
from datetime import datetime, timedelta

def fetch_time_entries(api_token, days=7):
    """
    Fetch time entries from Toggl for the last `days` days.
    Returns a list of entries, each with a 'project' field (project name).
    """
    since_dt = datetime.utcnow() - timedelta(days=days)
    since_unix = int(since_dt.timestamp())
    auth = (api_token, "api_token")
    # Fetch time entries
    url_entries = "https://api.track.toggl.com/api/v9/me/time_entries"
    params = {"since": since_unix}
    resp_entries = requests.get(url_entries, params=params, auth=auth)
    if resp_entries.status_code == 401:
        raise Exception("Unauthorized: Invalid Toggl API token.")
    if not resp_entries.ok:
        raise Exception(f"Toggl API error: {resp_entries.status_code} {resp_entries.text}")
    entries = resp_entries.json()

    # Fetch projects
    url_projects = "https://api.track.toggl.com/api/v9/me/projects"
    resp_projects = requests.get(url_projects, auth=auth)
    if not resp_projects.ok:
        # Don't fail if projects can't be fetched, just use Unknown Project
        project_map = {}
    else:
        projects = resp_projects.json()
        project_map = {p['id']: p['name'] for p in projects if 'id' in p and 'name' in p}

    # Attach project name to each entry
    for entry in entries:
        pid = entry.get('project_id')
        entry['project'] = project_map.get(pid, 'Unknown Project')
    return entries
