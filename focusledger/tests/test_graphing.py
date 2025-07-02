import pandas as pd
from focusledger.graphing import prepare_cumulative_graph

def test_prepare_cumulative_graph_empty():
    fig = prepare_cumulative_graph([])
    assert fig.layout.title.text == "No data available"

def test_prepare_cumulative_graph_basic():
    entries = [
        {"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T13:00:00+00:00", "stop": "2023-01-01T15:00:00+00:00", "project": "A"},
        {"start": "2023-01-02T10:00:00+00:00", "stop": "2023-01-02T11:00:00+00:00", "project": "A"},
        {"start": "2023-01-01T09:00:00+00:00", "stop": "2023-01-01T10:00:00+00:00", "project": "B"}
    ]
    fig = prepare_cumulative_graph(entries)
    assert "A" in fig.data[0].name or "B" in fig.data[0].name
    assert fig.layout.title.text == "Cumulative Time by Project"
