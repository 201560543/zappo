from web.database import Base, BaseMixin
import os

class Supplier(Base, BaseMixin):
    __tablename__="supplier"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
