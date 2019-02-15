import pytest
from app.database import db
from app.models import Mask

def test_init_database_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.database.init_database', fake_init_db)
    result = runner.invoke(args=['init-database'])
    assert 'Initialized' in result.output
    assert Recorder.called
