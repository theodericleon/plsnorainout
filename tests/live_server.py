import pathos.multiprocessing as multiprocessing
import socket
import time
import os
import socketserver
import unittest

from urllib.parse import urlparse, urljoin

import pytest
import os
import tempfile
from flask import Flask
import app
from app.db import get_db, init_db
from selenium import webdriver

"""
essentially the LiveServerTestCase class from flask-testing, but
using pathos multiprocessing instead (because Winders)
"""

class LiveServerTestCase(unittest.TestCase):
    def create_app(self):
        self.app = app.create_app({
            'TESTING': True,
            'LIVESERVER_TIMEOUT': 15
        })

    def __call__(self, result=None):
        self.app = self.create_app()

        self._configured_port = self.app.config.get('LIVESERVER_PORT', 5000)
        self._port_value = multiprocessing.Value('i', self._configured_port)

        self._ctx = self.app.test_request_context()
        self._ctx.push()

        try:
            self._spawn_live_server()
            super(LiveServerTestCase, self).__call__(result)
        finally:
            self._post_teardown()
            self._terminate_live_server()

    def get_server_url(self):
        return 'http://localhost:%s' % self._port_value.value

    def _spawn_live_server(self):
        self._process = None
        port_value = self._port_value

        def worker(app, port):
            original_socket_bind = socketserver.TCPServer.server_bind
            def socket_bind_wrapper(self):
                ret = original_socket_bind(self)

                (_, port) = self.socket.getsockname()
                port_value.value = port
                socketserver.TCPServer.server_bind = original_socket_bind
                return ret

            socketserver.TCPServer.server_bind = socket_bind_wrapper
            app.run(port=port, use_reloader=False)

        self._process = multiprocessing.Process(
            target=worker, args=(self.app, self._configured_port)
        )

        self._process.start()

        timeout = self.app.config.get('LIVESERVER_TIMEOUT', 5)
        start_time = time.time()

        while True:
            elapsed_time = (time.time() - start_time)
            if elapsed_time > timeout:
                raise RuntimeError(
                    "Failed to start the server after %d seconds. " % timeout
                )

            if self._can_ping_server():
                break

    def _can_ping_server(self):
        host, port = self._get_server_address()
        if port == 0:
            return False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
        except socket.error as e:
            success = False
        else:
            success = True
        finally:
            sock.close()

        return success

    def _get_server_address(self):
        parts = urlparse(self.get_server_url())

        host = parts.hostname
        port = parts.port

        if port is None:
            if parts.scheme == 'http':
                port = 80
            elif parts.scheme == 'https':
                port = 443
            else:
                raise RuntimeError(
                    "Unsupported server url scheme: %s" % parts.scheme
                )

        return host, port

    def _post_teardown(self):
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()
            del self._ctx

    def _terminate_live_server(self):
        if self._process:
            self._process.terminate()

class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):

        self.db_fd, self.db_path = tempfile.mkstemp()

        self.app.config['DATABASE'] = self.db_path

        with open(os.path.join(os.path.dirname(__file__), 'tests/data.sql'), 'rb') as f:
            _data_sql = f.read().decode('utf8')

        with self.app.app_context():
            init_db()
            get_db().executescript(_data_sql)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(driver_path='C:/Users/Derrick Milner/Documents/chromedriver.exe', chrome_options=chrome_options)

    def tearDown(self):
        self.driver.quit()
        os.close(self.db_fd)
        os.unlink(self.db_path)
