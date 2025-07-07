import os
from focusledger.toggl_api import fetch_time_entries

api_token = os.getenv("TOGGL_API_TOKEN")
entries = fetch_time_entries(api_token, days=30)
print(f"Number of entries: {len(entries)}")
for i, entry in enumerate(entries):
    print(f"Entry {i} keys: {list(entry.keys()) if isinstance(entry, dict) else type(entry)}")
    print(entry)
