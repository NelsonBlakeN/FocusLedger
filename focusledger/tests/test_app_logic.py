import pytest
from dash import Dash
from focusledger.app import app

def test_app_layout_exists():
    assert app.layout is not None
    assert hasattr(app, 'title')

def test_app_callback_outputs():
    # Simulate callback with no token
    import os
    from focusledger.app import update_graph
    # Temporarily clear the token
    old_token = os.environ.pop("TOGGL_API_TOKEN", None)
    try:
        result = update_graph(0, 7, 7)
        # Print result for debugging
        print("update_graph result:", result)
        # Should return error about missing token
        assert any("toggl api token not set" in str(x).lower() for x in result)
    finally:
        if old_token is not None:
            os.environ["TOGGL_API_TOKEN"] = old_token
