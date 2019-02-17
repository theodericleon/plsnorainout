import pytest
from app.database import db, init_database
from app.database_utils import populate_database
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

def test_populate_database_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_pop_db():
        Recorder.called = True

    monkeypatch.setattr('app.database_utils.populate_database', fake_pop_db)
    result = runner.invoke(args=['populate-database'])
    assert 'Populated' in result.output
    assert Recorder.called

def test_populate_database_function(app):
    with app.app_context():
        init_database()
        populate_database()
        assert Mask.query.count() == 2
