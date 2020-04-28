from web.database import Base

class Country(Base):
    __tablename__ = 'country'

    def __str__(self):
        return str(self.__dict__)
    