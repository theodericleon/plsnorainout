import pytest
from flask import g, session
from app.models import User

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username' : 'a', 'password' : 'a', 'zip_code' : '22222'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None

@pytest.mark.parametrize(('username', 'password','zip_code', 'message'), [
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Password is required.'),
    ('a', 'a', '', b'Zip code is required.'),
    ('test', 'test', '11111', b'already registered'),
])
def test_register_validate_input(client, username, password, zip_code, message):
    response = client.post(
        '/auth/register',
        data={'username' : username, 'password' : password, 'zip_code' : zip_code}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/dashboard'

    with client:
        client.get('/dashboard')
        assert session['user_id'] == 1
        assert g.user.username == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), [
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
])
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        response = auth.logout()
        assert 'user_id' not in session
        assert response.headers['Location'] == 'http://localhost/'
