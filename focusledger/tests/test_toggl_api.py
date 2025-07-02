import os
import pytest
from focusledger.toggl_api import fetch_time_entries

class MockResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or []
        self.text = text
        self.ok = status_code == 200
    def json(self):
        return self._json

def test_fetch_time_entries_success(monkeypatch):
    def mock_get(url, params, auth):
        return MockResponse(200, json_data=[{"id": 1, "start": "2023-01-01T10:00:00+00:00", "stop": "2023-01-01T12:00:00+00:00", "project": "Test Project"}])
    monkeypatch.setattr("requests.get", mock_get)
    entries = fetch_time_entries("dummy_token", days=1)
    assert len(entries) == 1
    assert entries[0]["project"] == "Test Project"

def test_fetch_time_entries_unauthorized(monkeypatch):
    def mock_get(url, params, auth):
        return MockResponse(401, text="Unauthorized")
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(Exception) as exc:
        fetch_time_entries("bad_token", days=1)
    assert "Unauthorized" in str(exc.value)

def test_fetch_time_entries_api_error(monkeypatch):
    def mock_get(url, params, auth):
        return MockResponse(500, text="Internal Server Error")
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(Exception) as exc:
        fetch_time_entries("token", days=1)
    assert "Toggl API error" in str(exc.value)
