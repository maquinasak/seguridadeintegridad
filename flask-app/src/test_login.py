import pytest

from app import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    return client


def test_hello(client):
    response = client.get('/usuarios', json={})
    json_data = response.json
    assert response.status_code == 200
    assert json_data["rta"] == 'ok'


