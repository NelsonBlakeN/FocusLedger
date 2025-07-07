import pandas as pd
from focusledger.graphing import prepare_cumulative_graph, prepare_rolling_average_graph

def test_prepare_cumulative_graph_empty():
    fig = prepare_cumulative_graph([])
    assert fig.layout.title.text == "No data available"

def test_prepare_cumulative_graph_with_projects_and_colors():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project_id": 1},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T12:00:00+00:00", "project_id": 2},
    ]
    projects = [
        {"id": 1, "name": "Alpha", "color": "#ff0000"},
        {"id": 2, "name": "Beta", "color": "#00ff00"},
    ]
    fig = prepare_cumulative_graph(entries, projects, days_to_show=2, rolling_window=1)
    # Check that the correct project names are used
    names = [t.name for t in fig.data]
    assert "Alpha" in names and "Beta" in names
    # Check that the colors are set
    colors = [t.line.color for t in fig.data]
    assert "#ff0000" in colors and "#00ff00" in colors

def test_prepare_cumulative_graph_rolling_window():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T13:00:00+00:00", "project": "A"},
        {"start": "2023-01-03T10:00:00+00:00", "stop": "2023-01-03T11:00:00+00:00", "project": "A"},
    ]
    fig = prepare_cumulative_graph(entries, days_to_show=3, rolling_window=2)
    # Should have 3 points, each a 2-day rolling sum
    y_vals = list(fig.data[0].y)
    assert len(y_vals) == 3

def test_prepare_cumulative_graph_basic():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T13:00:00+00:00", "stop": "2023-01-01T15:00:00+00:00", "project": "A"},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T11:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T09:00:00+00:00", "stop": "2023-01-01T10:00:00+00:00", "project": "B"}
    ]
    fig = prepare_cumulative_graph(entries)
    names = [t.name for t in fig.data]
    assert "A" in names or "B" in names
    # The title will be the rolling window default (7)
    assert "Running Total" in fig.layout.title.text

# --- Advanced tests with mocking ---
import pytest
from unittest.mock import patch, MagicMock

def test_prepare_cumulative_graph_handles_invalid_dates():
    # Simulate entries with invalid date formats
    entries = [
        {"start": "not-a-date", "stop": "not-a-date", "project": "A"},
        {"start": None, "stop": None, "project": "B"},
    ]
    fig = prepare_cumulative_graph(entries)
    # Should gracefully handle and show no data
    assert fig.layout.title.text == "No data available"

def test_prepare_cumulative_graph_handles_missing_project_info():
    # Simulate entries with missing project info
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00"},
    ]
    fig = prepare_cumulative_graph(entries)
    # Should fallback to 'Unknown Project' or similar
    names = [t.name for t in fig.data]
    assert any("Unknown" in n or n == "" for n in names)

def test_prepare_cumulative_graph_project_color_fallback():
    # Simulate project with no color
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project_id": 1},
    ]
    projects = [
        {"id": 1, "name": "Alpha"},  # No color field
    ]
    fig = prepare_cumulative_graph(entries, projects)
    # Should use a default color (e.g., any valid hex)
    color = fig.data[0].line.color
    assert isinstance(color, str) and color.startswith("#") and len(color) in (4, 7)

def test_prepare_cumulative_graph_handles_large_number_of_projects():
    # Simulate many projects to test color assignment and legend
    entries = []
    projects = []
    for i in range(20):
        entries.append({
            "start": f"2023-01-01T10:00:00+00:00",
            "stop": f"2023-01-01T11:00:00+00:00",
            "project_id": i
        })
        projects.append({"id": i, "name": f"Project {i}", "color": f"#%02x%02x%02x" % (i*10%256, i*5%256, i*3%256)})
    fig = prepare_cumulative_graph(entries, projects)
    # Should have 20 traces
    assert len(fig.data) == 20

def test_prepare_rolling_average_graph_empty():
    fig = prepare_rolling_average_graph([])
    assert fig.layout.title.text == "No data available"

def test_prepare_rolling_average_graph_with_projects_and_colors():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project_id": 1},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T12:00:00+00:00", "project_id": 2},
    ]
    projects = [
        {"id": 1, "name": "Alpha", "color": "#ff0000"},
        {"id": 2, "name": "Beta", "color": "#00ff00"},
    ]
    fig = prepare_rolling_average_graph(entries, projects, days_to_show=2, rolling_window=1)
    names = [t.name for t in fig.data]
    assert "Alpha" in names and "Beta" in names
    colors = [t.line.color for t in fig.data]
    assert "#ff0000" in colors and "#00ff00" in colors

def test_prepare_rolling_average_graph_rolling_window():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T13:00:00+00:00", "project": "A"},
        {"start": "2023-01-03T10:00:00+00:00", "stop": "2023-01-03T11:00:00+00:00", "project": "A"},
    ]
    fig = prepare_rolling_average_graph(entries, days_to_show=3, rolling_window=2)
    y_vals = list(fig.data[0].y)
    assert len(y_vals) == 3

def test_prepare_rolling_average_graph_basic():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T13:00:00+00:00", "stop": "2023-01-01T15:00:00+00:00", "project": "A"},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T11:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T09:00:00+00:00", "stop": "2023-01-01T10:00:00+00:00", "project": "B"}
    ]
    fig = prepare_rolling_average_graph(entries)
    names = [t.name for t in fig.data]
    assert "A" in names or "B" in names
    assert "Rolling Average" in fig.layout.title.text or "Average" in fig.layout.title.text

def test_prepare_rolling_average_graph_handles_invalid_dates():
    entries = [
        {"start": "not-a-date", "stop": "not-a-date", "project": "A"},
        {"start": None, "stop": None, "project": "B"},
    ]
    fig = prepare_rolling_average_graph(entries)
    assert fig.layout.title.text == "No data available"

def test_prepare_rolling_average_graph_handles_missing_project_info():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00"},
    ]
    fig = prepare_rolling_average_graph(entries)
    names = [t.name for t in fig.data]
    assert any("Unknown" in n or n == "" for n in names)

def test_prepare_rolling_average_graph_project_color_fallback():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project_id": 1},
    ]
    projects = [
        {"id": 1, "name": "Alpha"},
    ]
    fig = prepare_rolling_average_graph(entries, projects)
    color = fig.data[0].line.color
    assert isinstance(color, str) and color.startswith("#") and len(color) in (4, 7)

def test_prepare_rolling_average_graph_handles_large_number_of_projects():
    entries = []
    projects = []
    for i in range(20):
        entries.append({
            "start": f"2023-01-01T10:00:00+00:00",
            "stop": f"2023-01-01T11:00:00+00:00",
            "project_id": i
        })
        projects.append({"id": i, "name": f"Project {i}", "color": f"#%02x%02x%02x" % (i*10%256, i*5%256, i*3%256)})
    fig = prepare_rolling_average_graph(entries, projects)
    assert len(fig.data) == 20

