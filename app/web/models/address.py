import os
from web.models.custom_base import CustomBase

class Address(CustomBase):
    __tablename__="address"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
    