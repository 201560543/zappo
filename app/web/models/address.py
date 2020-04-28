from web.database import Base, BaseMixin
import os

class Address(Base, BaseMixin):
    __tablename__="address"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'