import pytest
from focusledger.toggl_projects import fetch_projects

class MockResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or []
        self.text = text
        self.ok = status_code == 200
    def json(self):
        return self._json

def test_fetch_projects_success(monkeypatch):
    def mock_get(url, auth):
        return MockResponse(200, json_data=[{"id": 1, "name": "Alpha", "color": "#ff0000"}])
    monkeypatch.setattr("requests.get", mock_get)
    projects = fetch_projects("dummy_token")
    assert isinstance(projects, list)
    assert projects[0]["name"] == "Alpha"

def test_fetch_projects_unauthorized(monkeypatch):
    def mock_get(url, auth):
        return MockResponse(401, text="Unauthorized")
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(Exception) as exc:
        fetch_projects("bad_token")
    assert "Unauthorized" in str(exc.value)

def test_fetch_projects_rate_limit(monkeypatch):
    def mock_get(url, auth):
        return MockResponse(429, text="Rate limit")
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(Exception) as exc:
        fetch_projects("token")
    assert "rate limit".lower() in str(exc.value).lower()

def test_fetch_projects_api_error(monkeypatch):
    def mock_get(url, auth):
        return MockResponse(500, text="Internal Server Error")
    monkeypatch.setattr("requests.get", mock_get)
    with pytest.raises(Exception) as exc:
        fetch_projects("token")
    assert "Toggl API error" in str(exc.value)
