import os

from flask import Flask, redirect, url_for, render_template
from app.database import db, init_database_command

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/dev.db',
        SQLALCHEMY_TRACK_MODIFICATIONS='False'
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        #load the tes config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # test route
    @app.route('/testing')
    def testresponse():
        return('Testing! Testing! Testing!')

    # index page
    @app.route('/')
    def index():
        return render_template('index.html')

    # maintenance page
    @app.route('/maintenance')
    def maintenance():
        return render_template('maintenance.html')

    @app.route('/dashboard')
    def dashboard():
        return redirect(url_for('maintenance'))

    db.init_app(app)
    app.cli.add_command(init_database_command)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
