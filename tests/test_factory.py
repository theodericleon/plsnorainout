from app import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING':True}).testing

def test_testresponse(client):
    response = client.get('testing')
    assert response.data == b'Testing! Testing! Testing!'

def test_maintenance(client):
    response = client.get('maintenance')
    assert response.get('/maintenance').status_code == 200

def test_index(client, app):
    assert client.get('/').status_code == 200

def test_dashboard(client, app):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert response.headers['Location'] == 'http://localhost/maintenance'
