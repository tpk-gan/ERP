from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

DB = SQLAlchemy()

class ROLE(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"

class USER(UserMixin, DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256), unique=True, nullable=False)
    password = DB.Column(DB.String(256), nullable=False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('role.id'))
    role = DB.relationship('Role', backref='users')