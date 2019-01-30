import os
import tempfile
import time
import pathos.multiprocessing
import logging

import pytest
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'tests/data.sql'), 'rb') as f:
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

class LiveServer(object):
    def __init__(self, app, host, port, clean_stop=False):
        self.app = app
        self.port = port
        self.host = host
        self.clean_stop = clean_stop
        self._process = None

    def start(self):
        def worker(app, host, port):
            app.run(host=host, port=port, use_reloader=False, threaded=True)

        self._process = multiprocessing.Process(
            target=worker,
            args=(self.app, self.host, self.port)
        )
        self._process.start()

        timeout = 5
        while timeout > 0:
            time.sleep(1)
            try:
                urlopen(self.url())
                timeout = 0
            except URLError:
                timeout -= 1

    def url(self, url=''):
        return 'http://%s:%d%s' % (self.host, self.port, url)

    def stop(self):
        if self._process:
            if self.clean_stop and self._stop_cleanly():
                return
            if self._process.is_alive():
                self._process.terminate()

    def _stop_cleanly(self, timeout=5):
        try:
            os.kill(self._process.pid, signal.SIGINT)
            self._process.join(timeout)
            return True
        except Exception as ex:
            logging.error('Failed to join the live server process: %r', ex)
            return False

    def __repr__(self):
        return '<LiveServer listening at %s>' % self.url()
