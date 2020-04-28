import os
from web.database import Base
from web.models.mixin import BaseMixin

class Address(BaseMixin, Base):
    __tablename__="address"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
    