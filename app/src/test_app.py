from app import app
from mock import patch

import json
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_bad_url(client):
    response = client.get('/bad/malformed/nonexistent/url')
    assert response.status_code == 404


@patch('api.v1.routes.get_blacklist_status', return_value="malware|keylogger")
def test_safetycheck(mock_function, client):
    answer = {"url": "def.example.com:4000/woot?foo=bar",
              "status": "malware|keylogger"}

    response = client.get('/urlinfo/1/def.example.com:4000/woot?foo=bar')
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == answer
