from flask_sqlalchemy import SQLAlchemy
from web import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '<User {0}>'.format(self.firstName)
