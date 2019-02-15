import os
import tempfile

import pytest
from app import create_app
from app.database import db, init_database
from app.models import User, Mask

@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI':'sqlite:////tmp/test.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': 'False',
    })

    db.init_app(app)

    with app.app_context():
        init_database()
        mask1 = Mask(mask_name = 'Simplus Full Face', manufacturer = 'Fisher & Paykel', type = 'FullFace')
        mask2 = Mask(mask_name = 'AirFit N20', manufacturer = 'ResMed', type = 'NasalMask')
        db.session.add(mask1)
        db.session.add(mask2)
        test = User(username='test', password_hash='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', zip_code='11111', mask_id='1')
        other = User(username='other', password_hash='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', zip_code='99999', mask_id='2')
        db.session.add(test)
        db.session.add(other)
        db.session.commit()


    yield app

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
