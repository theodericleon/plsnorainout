import os

from flask import Flask, redirect, url_for, render_template

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
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

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
