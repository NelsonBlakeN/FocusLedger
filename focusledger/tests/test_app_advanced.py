import pytest
import dash
import os
from unittest.mock import patch
from focusledger.app import update_graph
from focusledger.toggl_api import RateLimitError

def test_update_graph_success(monkeypatch):
    # Patch environment variable to simulate token
    with patch.dict(os.environ, {"TOGGL_API_TOKEN": "dummy_token"}):
        # Patch fetch_time_entries and fetch_projects to return fake data
        with patch("focusledger.app.fetch_time_entries", return_value=[{"start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "A"}]), \
             patch("focusledger.app.fetch_projects", return_value=[{"id": 1, "name": "A", "color": "#ff0000"}]):
            fig, err_msg, err_open, banner_msg, banner_open = update_graph(0, 7, 7)
            assert hasattr(fig, "data")
            assert err_open is False
            assert banner_open is False

def test_update_graph_rate_limit(monkeypatch):
    with patch.dict(os.environ, {"TOGGL_API_TOKEN": "dummy_token"}):
        # Patch fetch_time_entries to raise RateLimitError
        with patch("focusledger.app.fetch_time_entries", side_effect=RateLimitError("Toggl API rate limit reached. Displaying partial data.")), \
             patch("focusledger.app.fetch_projects", return_value=[]):
            fig, err_msg, err_open, banner_msg, banner_open = update_graph(0, 7, 7)
            assert banner_open is True
            assert "rate limit" in banner_msg.lower()


def test_update_graph_general_error(monkeypatch):
    with patch.dict(os.environ, {"TOGGL_API_TOKEN": "dummy_token"}):
        # Patch fetch_time_entries to raise a generic error
        with patch("focusledger.app.fetch_time_entries", side_effect=Exception("Some error")), \
             patch("focusledger.app.fetch_projects", return_value=[]):
            fig, err_msg, err_open, banner_msg, banner_open = update_graph(0, 7, 7)
            assert err_open is True
            assert "some error" in err_msg.lower()
