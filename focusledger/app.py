import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from toggl_api import fetch_time_entries, RateLimitError
from graphing import prepare_cumulative_graph
from toggl_projects import fetch_projects

# Load environment variables from .env if present
load_dotenv()

TOGGL_API_TOKEN = os.getenv("TOGGL_API_TOKEN")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "FocusLedger"

app.layout = dbc.Container([
    html.H1("FocusLedger: Toggl Time Visualization"),
    dbc.Alert(id="rate-limit-banner", color="warning", is_open=False, style={"marginBottom": "10px"}),
    dbc.Alert(id="error-message", color="danger", is_open=False),
    dbc.Row([
        dbc.Col([
            html.Label("Days to show on graph:"),
            dcc.Input(id="days_to_show", type="number", value=7, min=1, max=90),
        ], width=3),
        dbc.Col([
            html.Label("Rolling window (days):"),
            dcc.Input(id="rolling_window", type="number", value=7, min=1, max=90),
        ], width=3),
        dbc.Col([
            html.Button("Refresh", id="refresh", n_clicks=0)
        ], width=2)
    ]),
    dcc.Loading([
        dcc.Graph(id="cumulative-graph")
    ])
], fluid=True)

@app.callback(
    Output("cumulative-graph", "figure"),
    Output("error-message", "children"),
    Output("error-message", "is_open"),
    Output("rate-limit-banner", "children"),
    Output("rate-limit-banner", "is_open"),
    Input("refresh", "n_clicks"),
    State("days_to_show", "value"),
    State("rolling_window", "value")
)
def update_graph(n_clicks, days_to_show, rolling_window):
    if not TOGGL_API_TOKEN:
        return dash.no_update, "Toggl API token not set. Please set TOGGL_API_TOKEN in your environment.", True, "", False
    try:
        # Fetch enough data to cover the rolling window for the earliest day shown
        entries = fetch_time_entries(TOGGL_API_TOKEN, days_to_show + rolling_window - 1)
        try:
            projects = fetch_projects(TOGGL_API_TOKEN)
        except Exception:
            projects = []
        fig = prepare_cumulative_graph(entries, projects, days_to_show, rolling_window)
        return fig, "", False, "", False
    except RateLimitError as e:
        try:
            entries = []
            projects = []
            fig = prepare_cumulative_graph(entries, projects, days_to_show, rolling_window)
        except Exception:
            fig = dash.no_update
        return fig, "", False, "⚠️ Could not retrieve all data from Toggl due to API rate limiting.", True
    except Exception as e:
        return dash.no_update, str(e), True, "", False

if __name__ == "__main__":
    app.run(debug=True)
