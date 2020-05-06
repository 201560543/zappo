from web.database import Base, BaseMixin
import os

class Organization(Base, BaseMixin):
    __tablename__="organization"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
