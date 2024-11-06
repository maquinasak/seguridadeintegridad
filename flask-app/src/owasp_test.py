import pytest

from app import app


@pytest.fixture(autouse=True)
def client():
    app.testing = True
    global client
    client = app.test_client()

# 
# sql injection
# 

def test_get_usuarios_inject():
    response = client.get("/usuarios/'pepe@gmail.com' or true", json={})
    json_data = response.json
    print(json_data)
    assert response.status_code == 200
    assert json_data["rta"] == 'ok'

def test_check_inject():    
    response = client.get("/check/127.0.0.1&ls", json={})
    json_data = response.json
    print(json_data)
    assert response.status_code == 200

