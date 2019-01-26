import os
import tempfile
import time
import multiprocessing
import socket
import signal
import logging

import pytest
from flask import Flask
from flask_testing import LiveServerTestCase
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username' : username, 'password' : password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
        return AuthActions(client)

class LiveServer(LiveServerTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 15

        with app.app_context():
            init_db()
            get_db().executescript(_data_sql)

        return app

@pytest.fixture
def live_server():
    return LiveServer()

@pytest.fixture
def sel_driver(client, live_server):
    from selenium import webdriver
    sel_driver = webdriver.Chrome('C:/Users/Derrick Milner/Documents/chromedriver.exe')
    sel_driver.get('http://localhost/:5000')
    yield sel_driver
    sel_driver.quit()
