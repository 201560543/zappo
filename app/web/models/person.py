from web.database import Base, BaseMixin
import os

class Person(Base, BaseMixin):
    __tablename__="person"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
