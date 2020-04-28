from web.database import Base, BaseMixin
import os

class Account(Base, BaseMixin):
    __tablename__="account"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'