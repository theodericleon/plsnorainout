from app.database import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    zip_code = db.Column(db.Integer, nullable = False)

class Mask(db.Model):
    __tablename__ = 'masks'

    id = db.Column(db.Integer, primary_key = True)
    mask_name = db.Column(db.String(60), nullable = False)
    manufacturer = db.Column(db.String(60), nullable = False)
    type = db.Column(db.String(60), nullable = False)
