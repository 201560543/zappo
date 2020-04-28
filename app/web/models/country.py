from web.database import Base
from web.models.mixin import BaseMixin

class Country(BaseMixin, Base):
    __tablename__ = 'country'
    