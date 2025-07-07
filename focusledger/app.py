import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from focusledger.toggl_api import fetch_time_entries
from focusledger.graphing import prepare_cumulative_graph

# Load environment variables from .env if present
load_dotenv()

TOGGL_API_TOKEN = os.getenv("TOGGL_API_TOKEN")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "FocusLedger"

app.layout = dbc.Container([
    html.H1("FocusLedger: Toggl Time Visualization"),
    dbc.Alert(id="error-message", color="danger", is_open=False),
    dbc.Row([
        dbc.Col([
            html.Label("Days to show:"),
            dcc.Input(id="days", type="number", value=7, min=1, max=90),
            html.Button("Refresh", id="refresh", n_clicks=0)
        ], width=4)
    ]),
    dcc.Loading([
        dcc.Graph(id="cumulative-graph")
    ])
], fluid=True)

@app.callback(
    Output("cumulative-graph", "figure"),
    Output("error-message", "children"),
    Output("error-message", "is_open"),
    Input("refresh", "n_clicks"),
    State("days", "value")
)
def update_graph(n_clicks, days):
    if not TOGGL_API_TOKEN:
        return dash.no_update, "Toggl API token not set. Please set TOGGL_API_TOKEN in your environment.", True
    try:
        entries = fetch_time_entries(TOGGL_API_TOKEN, days)
        fig = prepare_cumulative_graph(entries)
        return fig, "", False
    except Exception as e:
        return dash.no_update, str(e), True

if __name__ == "__main__":
    # Listen on all interfaces so the app is accessible from other machines in the network (e.g., via Tailscale IP)
    app.run(debug=True, host="0.0.0.0", port=8050)
