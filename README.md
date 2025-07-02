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

5. Run the app locally:
   ```bash
   python focusledger/app.py
   ```

### Deploying to Heroku

1. Commit all changes to your repository and push to GitHub.
2. [Create a Heroku account](https://signup.heroku.com/) if you don't have one.
3. Go to the [Heroku Dashboard](https://dashboard.heroku.com/) and click **New > Create new app**.
4. Give your app a name and choose a region.
5. Under **Deploy**, connect your GitHub repository to Heroku.
6. Enable **Automatic Deploys** (optional) and click **Deploy Branch** to deploy manually.
7. Go to the **Settings** tab and click **Reveal Config Vars**. Add your `TOGGL_API_TOKEN` as a config var.
8. Your app will be available at `https://<your-app-name>.herokuapp.com` after the build completes.

**Heroku requirements:**
- The repository must have a `Procfile` (already included).
- The repository must have a `requirements.txt` (already included).
- The repository must have a `runtime.txt` specifying the Python version (already included).

**Note:** If you use the Heroku UI, you do not need to use the Heroku CLI for any step above.

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
