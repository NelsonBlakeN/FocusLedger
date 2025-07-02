from focusledger.app import app

def test_dash_app_exists():
    assert app is not None
    assert hasattr(app, 'layout')
