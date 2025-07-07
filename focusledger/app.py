import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from focusledger.toggl_api import fetch_time_entries, RateLimitError
from focusledger.graphing import prepare_cumulative_graph, prepare_rolling_average_graph, prepare_rolling_avg_of_sum_graph
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
                    html.Label("Cumulative: Days to show", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="days_to_show", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Cumulative: Rolling window (days)", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="rolling_window", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Average: Days to show", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="avg_days_to_show", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Average: Rolling window (days)", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="avg_rolling_window", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Avg of Sums: Days to show", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="sumavg_days_to_show", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Sum Window (days)", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="sum_window", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
                dbc.Col([
                    html.Label("Avg Window (days)", style={"fontWeight": "500", "color": "#4a4e69"}),
                    dcc.Input(id="avg_window", type="number", value=7, min=1, max=90, style={"width": "100%", "borderRadius": "8px", "border": "1px solid #c9ada7", "padding": "6px"}),
                ], width=2),
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
        ], style={"boxShadow": "0 2px 12px rgba(34,34,59,0.08)", "borderRadius": "16px", "backgroundColor": "#fff", "marginBottom": "2em"}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="average-graph", config={"displayModeBar": False})
            ])
        ], style={"boxShadow": "0 2px 12px rgba(34,34,59,0.08)", "borderRadius": "16px", "backgroundColor": "#fff", "marginBottom": "2em"}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="sumavg-graph", config={"displayModeBar": False})
            ])
        ], style={"boxShadow": "0 2px 12px rgba(34,34,59,0.08)", "borderRadius": "16px", "backgroundColor": "#fff"})
    ], type="circle"),
], fluid=True, style={"paddingTop": "2em", "paddingBottom": "2em", "backgroundColor": "#f8f8fa", "minHeight": "100vh"})


# Callback for both graphs

@app.callback(
    Output("cumulative-graph", "figure"),
    Output("average-graph", "figure"),
    Output("sumavg-graph", "figure"),
    Output("error-message", "children"),
    Output("error-message", "is_open"),
    Output("rate-limit-banner", "children"),
    Output("rate-limit-banner", "is_open"),
    Input("refresh", "n_clicks"),
    State("days_to_show", "value"),
    State("rolling_window", "value"),
    State("avg_days_to_show", "value"),
    State("avg_rolling_window", "value"),
    State("sumavg_days_to_show", "value"),
    State("sum_window", "value"),
    State("avg_window", "value")
)
def update_graphs(n_clicks, days_to_show, rolling_window, avg_days_to_show, avg_rolling_window, sumavg_days_to_show, sum_window, avg_window):
    token = os.getenv("TOGGL_API_TOKEN")
    if not token:
        return dash.no_update, dash.no_update, dash.no_update, "Toggl API token not set. Please set TOGGL_API_TOKEN in your environment.", True, "", False
    try:
        # Fetch enough data to cover the largest window needed for all graphs
        max_window = max(days_to_show + rolling_window - 1, avg_days_to_show + avg_rolling_window - 1, sumavg_days_to_show + sum_window + avg_window - 2)
        entries = fetch_time_entries(token, max_window)
        try:
            projects = fetch_projects(token)
        except Exception:
            projects = []
        fig_cum = prepare_cumulative_graph(entries, projects, days_to_show, rolling_window)
        fig_avg = prepare_rolling_average_graph(entries, projects, avg_days_to_show, avg_rolling_window)
        fig_sumavg = prepare_rolling_avg_of_sum_graph(entries, projects, sumavg_days_to_show, sum_window, avg_window)
        return fig_cum, fig_avg, fig_sumavg, "", False, "", False
    except RateLimitError as e:
        try:
            entries = []
            projects = []
            fig_cum = prepare_cumulative_graph(entries, projects, days_to_show, rolling_window)
            fig_avg = prepare_rolling_average_graph(entries, projects, avg_days_to_show, avg_rolling_window)
            fig_sumavg = prepare_rolling_avg_of_sum_graph(entries, projects, sumavg_days_to_show, sum_window, avg_window)
        except Exception:
            fig_cum = dash.no_update
            fig_avg = dash.no_update
            fig_sumavg = dash.no_update
        return fig_cum, fig_avg, fig_sumavg, "", False, "⚠️ Could not retrieve all data from Toggl due to API rate limiting.", True
    except Exception as e:
        return dash.no_update, dash.no_update, dash.no_update, str(e), True, "", False

if __name__ == "__main__":
    app.run(debug=True)
