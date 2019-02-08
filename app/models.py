from app import db

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    zip_code = db.Column(db.Integer, nullable = False)
