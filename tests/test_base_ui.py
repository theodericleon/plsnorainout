import pytest
import time
from flask import url_for

def test_nav_to_register(client, app, sel_driver):
    sel_driver.get('http://localhost/')
    sel_driver.find_element_by_id("register_link").click()
    time.sleep(1)
    assert sel_driver.current_url == 'http://localhost/auth/register'
