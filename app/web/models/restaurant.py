from web.database import Base, BaseMixin
import os

class Restaurant(Base, BaseMixin):
    __tablename__="restaurant"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
