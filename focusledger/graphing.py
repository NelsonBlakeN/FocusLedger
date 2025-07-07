import pandas as pd
import plotly.express as px
from datetime import datetime

def prepare_cumulative_graph(entries):
    if not entries:
        return px.line(title="No data available")
    # 'project' field is now set in fetch_time_entries; no need to patch here
    df = pd.DataFrame(entries)
    # Parse start/stop times
    df['start'] = pd.to_datetime(df['start'])
    df['stop'] = pd.to_datetime(df['stop'])
    df['duration'] = (df['stop'] - df['start']).dt.total_seconds() / 3600.0
    df['date'] = df['start'].dt.date
    df['project'] = df['project']
    # Group by project and date, sum durations
    grouped = df.groupby(['project', 'date'])['duration'].sum().reset_index()
    # Cumulative sum per project
    grouped['cumulative'] = grouped.groupby('project')['duration'].cumsum()
    fig = px.line(
        grouped,
        x='date',
        y='cumulative',
        color='project',
        markers=True,
        title="Cumulative Time by Project"
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Cumulative Hours")
    return fig
