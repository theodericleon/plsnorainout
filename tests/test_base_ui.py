import pytest
import urllib3
import time
import os
import tempfile
from flask import Flask
from flask_testing import LiveServerTestCase
from app import create_app
from app.db import get_db, init_db
"""
def test_nav_to_register(client, app, sel_driver):
    sel_driver.get('http://localhost/:5000')
    time.sleep(5)
"""
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

class LiveServer(LiveServerTestCase):
    def create_app(self):
        db_fd, db_path = tempfile.mkstemp()


        app = create_app({
            'TESTING': True,
            'DATABASE':db_path,
            'LIVESERVER_TIMEOUT':15
        })

        return app

    def setUp(self):
        with app.app_context():
            init_db()
            get_db().executescript(_data_sql)

        self.driver = webdriver.Chrome('C:/Users/Derrick Milner/Documents/chromedriver.exe')
        self.driver.get('http://localhost/:5000')

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        assert response.code == 200
