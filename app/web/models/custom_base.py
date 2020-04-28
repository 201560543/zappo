from web.database import Base

class CustomBase(Base):
    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}