import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from focusledger.toggl_api import fetch_time_entries, RateLimitError
from focusledger.graphing import prepare_cumulative_graph
from focusledger.toggl_projects import fetch_projects

# Load environment variables from .env if present
load_dotenv()



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "FocusLedger"

app.layout = dbc.Container([
    html.H1("FocusLedger: Toggl Time Visualization", style={
        "fontWeight": "bold",
        "fontSize": "2.5rem",
        "marginBottom": "0.5em",
        "color": "#22223b",
        "letterSpacing": "-1px"
    }),
    dbc.Alert(id="rate-limit-banner", color="warning", is_open=False, style={"marginBottom": "10px"}),
    dbc.Alert(id="error-message", color="danger", is_open=False),
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Days to show on graph:", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="days_to_show", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=3),
                dbc.Col([
                    html.Label("Rolling window (days):", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="rolling_window", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=3),
                dbc.Col([
                    html.Button("Refresh", id="refresh", n_clicks=0, className="btn btn-primary", style={"width": "100%", "borderRadius": "8px", "backgroundColor": "#22223b", "border": "none", "fontWeight": "bold"})
                ], width=2),
            ], align="center", style={"marginBottom": "0.5em"}),
        ])
    ], style={"boxShadow": "0 2px 12px rgba(34,34,59,0.08)", "borderRadius": "16px", "marginBottom": "1.5em", "backgroundColor": "#f8f8fa"}),
    dcc.Loading([
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="cumulative-graph", config={"displayModeBar": False})
            ])
        ], style={"boxShadow": "0 2px 12px rgba(34,34,59,0.08)", "borderRadius": "16px", "backgroundColor": "#fff"})
    ], type="circle"),
], fluid=True, style={"paddingTop": "2em", "paddingBottom": "2em", "backgroundColor": "#f8f8fa", "minHeight": "100vh"})

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
    token = os.getenv("TOGGL_API_TOKEN")
    if not token:
        return dash.no_update, "Toggl API token not set. Please set TOGGL_API_TOKEN in your environment.", True, "", False
    try:
        # Fetch enough data to cover the rolling window for the earliest day shown
        entries = fetch_time_entries(token, days_to_show + rolling_window - 1)
        try:
            projects = fetch_projects(token)
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
