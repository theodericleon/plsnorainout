import live_server
import pytest
import time
import urllib3

class BaseUITests(live_server.SeleniumTestCase):

    def create_app(self):
        super()

    def setUp(self):
        super()

    def tearDown(self):
        super()

    def test_server_is_up_and_running(self):
        response = urllib3.urlopen(self.get_server_url())
        assert response.code == 200

    def test_nav_to_register(self):
        self.driver.get('http://localhost/:5000')
        time.sleep(5)
        self.driver.find_element_by_id("register_link").click()
        assert self.driver.current_url == 'http://localhost/auth/register'
