import pytest
from dash import Dash
from focusledger.app import app

def test_app_layout_exists():
    assert app.layout is not None
    assert hasattr(app, 'title')
