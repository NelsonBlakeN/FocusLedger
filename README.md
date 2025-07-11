# FocusLedger

FocusLedger is a Python Dash web application for visualizing time tracked in Toggl. It generates interactive graphs of cumulative time spent on projects, grouped by project, over a configurable time window.

## Features
- Fetches Toggl time entries and groups by project
- Interactive graphs:
  - **Cumulative Time Graph:** Running total of hours per project over a rolling window and date range
  - **Rolling Average Graph:** Rolling average of hours per day per project, with sum of all project averages per day
  - **Rolling Avg of Sums Graph:** Rolling average of rolling sums for each project, and sum of these for each day
- Configurable date range and rolling window for each graph (independent controls)
- Project colors from Toggl
- Secure: Toggl API token via environment variable
- Unit tests for all graphing logic
- Simple deployment on Google Cloud VM using systemd service

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



### Deployment on Google Cloud VM

FocusLedger is deployed on a Google Cloud VM for simplicity and reliability. The app runs as a systemd service using the provided `focus-ledger.service` file. This approach avoids the complexity of platform-specific hosting and gives full control over the environment.

**Deployment steps:**

1. Set up a Google Cloud VM (Ubuntu recommended).
2. Clone this repository and set up your Python environment as above.
3. Copy your `.env` file with the Toggl API token.
4. Install required Python packages:

   ```bash
   bash install.sh
   ```

5. Copy `focus-ledger.service` to `/etc/systemd/system/` and edit paths as needed.
6. Enable and start the service:

   ```bash
   sudo systemctl enable focus-ledger
   sudo systemctl start focus-ledger
   ```

7. Access the app via the VM's public IP and configured port.

**Files for deployment:**

- `focus-ledger.service`: systemd service file for running the app
- `requirements.txt`, `install.sh`: Python dependencies and setup


### Running Tests

```bash
pytest
```



### Deployment Notes

- Set the `TOGGL_API_TOKEN` environment variable in your deployment environment.
- Deploy as a standard Dash app using systemd for process management.


## Code Structure

- `focusledger/app.py`: Main Dash app (UI, callbacks, all graphs)
- `focusledger/toggl_api.py`: Toggl API client
- `focusledger/graphing.py`: Data processing and plotting (cumulative, rolling average, rolling avg of sums)
- `focusledger/tests/`: Unit tests for graphing and API logic
## Usage

When you run the app, you will see two graphs:

1. **Cumulative Time Graph**
   - Shows the running total of hours per project over a rolling window.
   - Controls: "Cumulative: Days to show" and "Cumulative: Rolling window (days)".

2. **Rolling Average Graph**
   - Shows the rolling average of hours per day for each project, over a rolling window.
   - Controls: "Average: Days to show" and "Average: Rolling window (days)".
   - The sum of all project averages is shown in the hover for each day.

You can adjust the controls for each graph independently and click **Refresh** to update the data and graphs.

---



For more details, see the project plan in `PROJECT_PLAN.md`.
