from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean)
    access_permission = db.Column(db.Boolean)

class LogAccess( db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_access = db.Column(db.String(200))

class Room(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room = db.Column(db.String(200))