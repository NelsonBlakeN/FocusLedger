# FocusLedger

FocusLedger is a Python Dash web application for visualizing time tracked in Toggl. It generates interactive graphs of cumulative time spent on projects, grouped by project, over a configurable time window.

## Features
- Fetches Toggl time entries and groups by project
- Interactive line graph of cumulative time
- Configurable date range (default: 7 days)
- Secure: Toggl API token is provided via environment variable
- Easily deployable to Heroku, Render, Vercel, etc.

## Getting Started

### Prerequisites
- Python 3.8+
- A Toggl API token

### Setup
1. Clone this repository.
2. Copy `.env.example` to `.env` and add your Toggl API token.
3. Run the install script to set up a local Python environment and install dependencies:
   ```bash
   bash install.sh
   ```
4. Activate the environment (if not already active):
   ```bash
   source .venv/bin/activate
   ```
5. Run the app:
   ```bash
   python focusledger/app.py
   ```

### Running Tests
```bash
pytest
```

### Deployment
- Set the `TOGGL_API_TOKEN` environment variable in your deployment environment.
- Deploy as a standard Dash app (see deployment guides for Heroku, Render, etc.)

## Code Structure
- `focusledger/app.py`: Main Dash app
- `focusledger/toggl_api.py`: Toggl API client
- `focusledger/graphing.py`: Data processing and plotting
- `focusledger/tests/`: Unit tests

---

For more details, see the project plan in `PROJECT_PLAN.md`.
