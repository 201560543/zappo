from web.database import Base, BaseMixin
import os

class AddressType(Base, BaseMixin):
    __tablename__="address_type"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
