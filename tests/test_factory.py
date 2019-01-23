from plsnorainout import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING':True}).testing

def test_maintenance(client):
    response = client.get('maintenance')
    assert response.data == b'Under maintenance, come back soon!'
