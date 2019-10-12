from flask_login import UserMixin
from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy import func

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

    def __init__(self,roles):
        self.roles

    def has_role(self, list_roles):
        return any(role.name for role in self.roles if role.name in list_roles)

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
    dt_start_access = db.Column(db.String(1000))
    dt_end_access = db.Column(db.String(1000))

    # def __init__(self, room_id, user_id, dt_access, hours_id, description, dt_start_access, dt_end_access):
    #     self.dt_start_access = dt_start_access
    #     self.dt_end_access = dt_end_access

    @hybrid_property
    def datetime_start_access(self):
        return datetime.strptime(self.dt_start_access, '%d/%m/%Y %H:%M:%S')

    @datetime_start_access.expression
    def datetime_start_access(cls):
        dt_column =(func.substr(cls.dt_start_access, 7, 4) + "-" + func.substr(cls.dt_start_access, 4, 2) + "-" + func.substr(cls.dt_start_access, 1, 2) + ' ' + func.substr(cls.dt_start_access, 12) )
        dt_column = func.datetime(dt_column)
        return dt_column

    @hybrid_property
    def datetime_end_access(self):
        return datetime.strptime(self.dt_end_access, '%d/%m/%Y %H:%M:%S')

    @datetime_end_access.expression
    def datetime_end_access(cls):
        dt_column =(func.substr(cls.dt_end_access, 7, 4) + "-" + func.substr(cls.dt_end_access, 4, 2) + "-" + func.substr(cls.dt_end_access, 1, 2) + ' ' + func.substr(cls.dt_end_access, 12) )
        dt_column = func.datetime(dt_column)
        return dt_column

class LogAccess(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    room_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_access = db.Column(db.String(200))
