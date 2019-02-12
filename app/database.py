from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_database():

    with current_app.app_context():
        db.drop_all()
        db.create_all()

@click.command('init-database')
@with_appcontext
def init_database_command():
    """Clear the exisiting data and create new tables."""
    init_database()
    click.echo('Initialized the database.')
