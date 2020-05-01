from web.database import Base, BaseMixin
import os

class Country(Base, BaseMixin):
    __tablename__ = 'country'
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
    