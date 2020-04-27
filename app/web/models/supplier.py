from flask_sqlalchemy import SQLAlchemy
from web.database import db
import os

class Supplier(db.Model):
    __tablename__="supplier"

    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(100), default='')
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), default='')
    is_deleted = db.Column(db.Integer, nullable=False, default=0)
    logo_path = db.Column(db.String(100), default='')
    url = db.Column(db.String(100), default='')

    def __repr__(self):
        return f'''{[
            self.id,
            self.organization_id,
            self.supplier_name,
            self.business_name,
            self.created_at,
            self.updated_at,
            self.is_deleted,
            self.logo_path,
            self.url
            ]}'''