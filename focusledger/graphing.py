def prepare_rolling_average_graph(entries, projects=None, days_to_show=7, rolling_window=7):
    """
    Prepares a rolling average graph for each project, showing the average hours per day over a rolling window.
    The graph displays the rolling average for each project and the sum of these averages for each day.
    """
    try:
        if not entries:
            return px.line(title="No data available")
        df = pd.DataFrame(entries)
        project_map = {}
        color_map = {}
        if projects:
            for proj in projects:
                project_map[proj.get('id')] = proj.get('name', str(proj.get('id')))
                if 'color' in proj and proj['color']:
                    color_map[proj.get('name', str(proj.get('id')))] = proj['color']
        if 'project_id' in df.columns:
            df['project'] = df['project_id'].map(lambda pid: project_map.get(pid, str(pid)) or "Unknown Project")
        elif 'project' in df.columns:
            df['project'] = df['project'].fillna('Unknown Project')
            df.loc[df['project'] == '', 'project'] = 'Unknown Project'
        else:
            df['project'] = 'Unknown Project'
        df['project'] = df['project'].fillna('Unknown Project')
        df['start'] = pd.to_datetime(df['start'], errors='coerce')
        df['stop'] = pd.to_datetime(df['stop'], errors='coerce')
        df = df.dropna(subset=['start', 'stop'])
        if df.empty:
            return px.line(title="No data available")
        df['duration'] = (df['stop'] - df['start']).dt.total_seconds() / 3600.0
        df['date'] = df['start'].dt.date
        if df['date'].empty:
            return px.line(title="No data available")
        all_dates = pd.date_range(df['date'].min(), df['date'].max())
        result = []
        for project in df['project'].unique():
            proj_df = df[df['project'] == project]
            for date in all_dates:
                window_start = date - pd.Timedelta(days=rolling_window-1)
                date_only = date.date()
                window_start_only = window_start.date()
                mask = (proj_df['date'] >= window_start_only) & (proj_df['date'] <= date_only)
                days_in_window = (date_only - window_start_only).days + 1
                total = proj_df.loc[mask, 'duration'].sum()
                avg = total / days_in_window if days_in_window > 0 else 0
                result.append({'project': project, 'date': date_only, 'rolling_avg': avg})
        result_df = pd.DataFrame(result)
        if not result_df.empty:
            last_date = result_df['date'].max()
            if isinstance(last_date, datetime):
                last_date = last_date.date()
            cutoff = last_date - pd.Timedelta(days=days_to_show-1)
            if isinstance(cutoff, pd.Timestamp):
                cutoff = cutoff.date()
            result_df = result_df[result_df['date'] >= cutoff]
        result_df['hover_hours'] = result_df['rolling_avg'].round(2).astype(str) + ' avg hrs/day'
        # Compute sum of averages for each date
        sum_avg_by_date = result_df.groupby('date')['rolling_avg'].sum().round(2).astype(str) + ' total avg hrs/day'
        sum_map = sum_avg_by_date.to_dict()
        result_df['sum_avg_for_day'] = result_df['date'].map(sum_map)
        fig = px.line(
            result_df,
            x='date',
            y='rolling_avg',
            color='project',
            markers=True,
            title=f"{rolling_window}-Day Rolling Average by Project",
            custom_data=['project', 'hover_hours', 'sum_avg_for_day']
        )
        if color_map:
            for trace in fig.data:
                proj_name = trace.name
                if proj_name in color_map:
                    trace.line.color = color_map[proj_name]
        for trace in fig.data:
            trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
            trace.mode = "lines+markers"
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=f"Avg Hours/Day ({rolling_window}-day window)",
            hovermode="x unified",
            hoverlabel=dict(namelength=0)
        )
        for i, trace in enumerate(fig.data):
            if i == 0:
                trace.hovertemplate = (
                    "<b>Sum of Avgs: %{customdata[2]}</b><br>"
                    "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
                )
            else:
                trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
        return fig
    except Exception:
        return px.line(title="No data available")
import pandas as pd
import plotly.express as px
from datetime import datetime

def prepare_cumulative_graph(entries, projects=None, days_to_show=7, rolling_window=7):
    try:
        if not entries:
            return px.line(title="No data available")
        df = pd.DataFrame(entries)
        # Map project_id to project name if possible
        project_map = {}
        color_map = {}
        if projects:
            for proj in projects:
                project_map[proj.get('id')] = proj.get('name', str(proj.get('id')))
                # Toggl color is a hex string in 'color' field, e.g. '#ff0000'
                if 'color' in proj and proj['color']:
                    color_map[proj.get('name', str(proj.get('id')))] = proj['color']
        if 'project_id' in df.columns:
            df['project'] = df['project_id'].map(lambda pid: project_map.get(pid, str(pid)) or "Unknown Project")
        elif 'project' in df.columns:
            # Use the project field directly if present
            df['project'] = df['project'].fillna('Unknown Project')
            df.loc[df['project'] == '', 'project'] = 'Unknown Project'
        else:
            df['project'] = 'Unknown Project'
        df['project'] = df['project'].fillna('Unknown Project')
        # Parse start/stop times
        df['start'] = pd.to_datetime(df['start'], errors='coerce')
        df['stop'] = pd.to_datetime(df['stop'], errors='coerce')
        # Remove rows with invalid dates
        df = df.dropna(subset=['start', 'stop'])
        if df.empty:
            return px.line(title="No data available")
        df['duration'] = (df['stop'] - df['start']).dt.total_seconds() / 3600.0
        df['date'] = df['start'].dt.date
        # Build a date range for the graph (last N days)
        if df['date'].empty:
            return px.line(title="No data available")
        all_dates = pd.date_range(df['date'].min(), df['date'].max())
        # For each project, calculate rolling sum for each day
        result = []
        for project in df['project'].unique():
            proj_df = df[df['project'] == project]
            for date in all_dates:
                window_start = date - pd.Timedelta(days=rolling_window-1)
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
            cutoff = last_date - pd.Timedelta(days=days_to_show-1)
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
            title=f"{rolling_window}-Day Running Total by Project",
            custom_data=['project', 'hover_hours', 'total_for_day']
        )

        # Set project colors from Toggl
        if color_map:
            for trace in fig.data:
                proj_name = trace.name
                if proj_name in color_map:
                    trace.line.color = color_map[proj_name]

        # Custom hover for single points: just project and value, no labels
        for trace in fig.data:
            trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
            trace.mode = "lines+markers"

        # Custom hover for x unified: show total and all projects for that day
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=f"Hours ({rolling_window}-day running total)",
            hovermode="x unified",
            hoverlabel=dict(namelength=0)
        )

        # Add a visible annotation for the total at the top of the unified hover
        for i, trace in enumerate(fig.data):
            if i == 0:
                trace.hovertemplate = (
                    "<b>Total: %{customdata[2]}</b><br>"
                    "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
                )
            else:
                trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"

        return fig
    except Exception:
        return px.line(title="No data available")
        last_date = result_df['date'].max()
        if isinstance(last_date, datetime):
            last_date = last_date.date()
        cutoff = last_date - pd.Timedelta(days=days_to_show-1)
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
        title=f"{rolling_window}-Day Running Total by Project",
        custom_data=['project', 'hover_hours', 'total_for_day']
    )

    # Set project colors from Toggl
    if color_map:
        for trace in fig.data:
            proj_name = trace.name
            if proj_name in color_map:
                trace.line.color = color_map[proj_name]

    # Custom hover for single points: just project and value, no labels
    for trace in fig.data:
        trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
        trace.mode = "lines+markers"

    # Custom hover for x unified: show total and all projects for that day
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"Hours ({rolling_window}-day running total)",
        hovermode="x unified",
        hoverlabel=dict(namelength=0)
    )

    # Add a visible annotation for the total at the top of the unified hover
    for i, trace in enumerate(fig.data):
        if i == 0:
            trace.hovertemplate = (
                "<b>Total: %{customdata[2]}</b><br>"
                "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"
            )
        else:
            trace.hovertemplate = "%{customdata[0]}<br>%{customdata[1]}<extra></extra>"

    return fig
