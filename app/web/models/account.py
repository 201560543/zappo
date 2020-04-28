import os
from web.database import Base
from web.models.mixin import BaseMixin
## TO DO: Delete bottom commonts
# from flask_sqlalchemy import SQLAlchemy
# from web.database import db

# class Account(db.Model):
#     __tablename__="account"
#     if os.environ.get('MYSQL_DB_BIND'):
#         __bind_key__ = 'mysql_db'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     organization_id = db.Column(db.Integer, nullable=False)
#     account_number = db.Column(db.String(32), nullable=False)
#     account_name = db.Column(db.String(50), nullable=False)
#     is_active = db.Column(db.Integer, nullable=False, default=1)
#     created_at = db.Column(db.DateTime(), nullable=False)
#     updated_at = db.Column(db.DateTime(), default='')
#     is_deleted = db.Column(db.Integer, nullable=False, default=0)
#     timezone_name = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f'''{[
#             self.id,
#             self.organization_id,
#             self.account_number,
#             self.account_name,
#             self.is_active,
#             self.created_at,
#             self.updated_at,
#             self.is_deleted,
#             self.timezone_name
#             ]}'''

class Account(BaseMixin, Base):
    __tablename__="account"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'