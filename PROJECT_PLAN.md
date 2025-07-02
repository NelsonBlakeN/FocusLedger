# FocusLedger: Project Plan

## Overview

FocusLedger is a single-page Python web application built with Dash that visualizes time logged on the Toggl platform. The core feature is to generate a line graph of cumulative time spent on projects, grouped by project, over a configurable time window (default: 7 days). All logic, including Toggl API calls and data processing, is handled client-side within the Dash app.


## Technology Stack

- **Frontend & Logic**: [Plotly Dash](https://dash.plotly.com/) for a single-page Python web app with interactive data visualization and UI.
- **HTTP Requests**: [requests](https://docs.python-requests.org/) for interacting with the Toggl API directly from the Dash app.
- **Testing**: [pytest](https://docs.pytest.org/) for unit and integration tests of data processing and API logic.
- **Deployment**: Easily deployable as a single Python web app to [Render](https://render.com/), [Heroku](https://www.heroku.com/), or [Vercel](https://vercel.com/) (using serverless Python support).


## Code Structure

```text
focusledger/
├── app.py             # Entry point for the Dash app (UI, callbacks, and logic)
├── toggl_api.py       # Toggl API client (fetches and processes time entries)
├── graphing.py        # Functions for preparing and plotting data
├── tests/
│   ├── test_toggl_api.py
│   ├── test_graphing.py
│   └── test_app.py
└── requirements.txt   # Python dependencies
```


## Credentials & Security

- **Toggl API Token**: Required to access Toggl data. The token is read from an environment variable (e.g., `TOGGL_API_TOKEN`) at runtime. For local development, a `.env` file can be used to set this variable. The token is never hardcoded or stored in the codebase, ensuring compatibility with 12-factor app design and secure deployment.


## Key Features

1. **Toggl API Token via Environment Variable**: The Toggl API token is read from an environment variable (e.g., `TOGGL_API_TOKEN`) at runtime. This allows the app to be run locally or in a deployed environment without code changes, following 12-factor app principles. For local development, a `.env` file can be used (not committed to version control).
2. **Fetch Toggl Data**: Retrieve time entries for a user, grouped by project, for a configurable date range, directly from the Dash app.
3. **Data Processing**: Aggregate and compute cumulative time per project per day.
4. **Graphing**: Generate a line graph (Plotly) showing cumulative time per project.
5. **Configurable UI**: Allow user to select date range and grouping options.
6. **Testing**: Unit tests for API client, data processing, and graphing logic.


## Error Handling

- If the API token is missing or invalid, the app will display a clear error and halt further processing.
- Any authorization errors from Toggl will be surfaced to the user for correction.


## Example Test Cases

- Fetching data with valid/invalid credentials (mocked for tests)
- No time entries in the selected range
- Multiple projects with overlapping time entries
- Edge cases: single project, single day, large date range
- Graph rendering with empty and non-empty datasets


## Next Steps

1. Await your approval or feedback on this revised plan.
2. Once approved, set up the project structure and implement the Dash app with secure token input and Toggl API client.
3. Prompt you to provide your Toggl API token in the app UI before proceeding with live API calls.
