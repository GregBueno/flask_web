from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    num_university = db.Column(db.Integer)
    access_permission = db.Column(db.Boolean)
    dt_start_access =  db.Column(db.String(200))
    dt_end_access = db.Column(db.String(200))

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Room(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room = db.Column(db.String(200))

class Hours(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    hour_start = db.Column(db.Integer)
    hour_end = db.Column(db.Integer)
    desc_hour = db.Column(db.String(1000))

class HourRegister(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    dt_access = db.Column(db.String(200))
    hours_id = db.Column(db.Integer)
    description = db.Column(db.String(1000))

class LogAccess(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_access = db.Column(db.String(200))
