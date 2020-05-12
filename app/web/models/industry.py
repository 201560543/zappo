from web.database import Base, BaseMixin
import os

class Industry(Base, BaseMixin):
    __tablename__="industry"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
