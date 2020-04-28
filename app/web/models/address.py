import os
from web.database import Base

class Address(Base):
    __tablename__="address"
    if os.environ.get('MYSQL_DB_BIND'):
        __bind_key__ = 'mysql_db'
    
    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}