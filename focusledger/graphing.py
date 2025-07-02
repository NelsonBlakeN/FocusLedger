import pandas as pd
import plotly.express as px
from datetime import datetime

def prepare_cumulative_graph(entries, projects=None, days=7):
    if not entries:
        return px.line(title="No data available")
    df = pd.DataFrame(entries)
    # Map project_id to project name if possible
    project_map = {}
    if projects:
        for proj in projects:
            project_map[proj.get('id')] = proj.get('name', str(proj.get('id')))
    if 'project_id' in df.columns:
        df['project'] = df['project_id'].map(lambda pid: project_map.get(pid, str(pid)))
    else:
        df['project'] = 'No Project'
    df['project'] = df['project'].fillna('No Project')
    # Parse start/stop times
    df['start'] = pd.to_datetime(df['start'])
    df['stop'] = pd.to_datetime(df['stop'])
    df['duration'] = (df['stop'] - df['start']).dt.total_seconds() / 3600.0
    df['date'] = df['start'].dt.date
    # Build a date range for the graph (last N days)
    all_dates = pd.date_range(df['date'].min(), df['date'].max())
    # For each project, calculate rolling 7-day sum for each day
    result = []
    for project in df['project'].unique():
        proj_df = df[df['project'] == project]
        for date in all_dates:
            window_start = date - pd.Timedelta(days=days-1)
            # Convert to date only once
            date_only = date.date()
            window_start_only = window_start.date()
            mask = (proj_df['date'] >= window_start_only) & (proj_df['date'] <= date_only)
            total = proj_df.loc[mask, 'duration'].sum()
            result.append({'project': project, 'date': date_only, 'rolling_sum': total})
    result_df = pd.DataFrame(result)
    # Only show the last N days on the graph
    if not result_df.empty:
        last_date = result_df['date'].max()
        if isinstance(last_date, datetime):
            last_date = last_date.date()
        cutoff = last_date - pd.Timedelta(days=days-1)
        if isinstance(cutoff, pd.Timestamp):
            cutoff = cutoff.date()
        result_df = result_df[result_df['date'] >= cutoff]
    # Format rolling_sum to 1 decimal and add units
    result_df['hover_hours'] = result_df['rolling_sum'].round(1).astype(str) + ' hours'

    # Compute total for each date for unified hover
    total_by_date = result_df.groupby('date')['rolling_sum'].sum().round(1).astype(str) + ' hours'
    total_map = total_by_date.to_dict()
    result_df['total_for_day'] = result_df['date'].map(total_map)

    fig = px.line(
        result_df,
        x='date',
        y='rolling_sum',
        color='project',
        markers=True,
        title=f"7-Day Running Total by Project",
        custom_data=['project', 'hover_hours', 'total_for_day']
    )

    # Custom hover for single points: just project and value, no labels
    for trace in fig.data:
        trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
        trace.mode = "lines+markers"

    # Custom hover for x unified: show total and all projects for that day
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Hours (7-day running total)",
        hovermode="x unified",
        hoverlabel=dict(namelength=0)
    )

    # Add a visible annotation for the total at the top of the unified hover
    # This workaround uses the hovertemplate to inject the total for the day at the top of the hover box
    # Only the first trace for each x value will show the total, others will show blank
    for i, trace in enumerate(fig.data):
        # Only show the total for the first project trace at each x value
        if i == 0:
            trace.hovertemplate = (
                "<b>Total: %{customdata[2]}</b><br>"  # total_for_day
                "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
            )
        else:
            trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"

    return fig
