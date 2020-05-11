from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

db = SQLAlchemy()
Base = automap_base()

class BaseMixin():
    """
    Base dunder methods and utility as_dict method for debugging and returning data for models
    """
    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}