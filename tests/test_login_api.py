import os
from werkzeug.security import generate_password_hash

# Ensure environment variables are set before importing the app
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('ADMIN_USERNAME', 'admin')
os.environ.setdefault('ADMIN_PASSWORD_HASH', generate_password_hash('password'))

import importlib
app_module = importlib.import_module('app')


def test_successful_login_sets_session_and_redirects():
    client = app_module.app.test_client()
    resp = client.post('/api/admin_login', json={'username': 'admin', 'password': 'password'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert 'redirect' in data

    # Follow the redirect URL using the same client (session cookie should be set)
    redirected = client.get(data['redirect'])
    assert redirected.status_code == 200


def test_failed_login_returns_401_and_message():
    client = app_module.app.test_client()
    resp = client.post('/api/admin_login', json={'username': 'admin', 'password': 'wrong'})
    assert resp.status_code == 401
    data = resp.get_json()
    assert data['success'] is False
    assert 'message' in data
