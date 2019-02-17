from flask import current_app
import click
from flask.cli import with_appcontext
from app.database import db
from app.models import Mask

def populate_database():
    with current_app.app_context():
        mask1 = Mask(mask_name = 'Simplus Full Face', manufacturer = 'Fisher & Paykel', type = 'FullFace')
        mask2 = Mask(mask_name = 'AirFit N20', manufacturer = 'ResMed', type = 'NasalMask')
        db.session.add(mask1)
        db.session.add(mask2)
        db.session.commit()

@click.command('populate-database')
@with_appcontext
def populate_database_command():
    populate_database()
    click.echo('Populated the database.')
