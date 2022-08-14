from sqlalchemy import Column, Integer, LargeBinary, String
from databases.base import Base


class Country(Base):
    __tablename__ = "Country"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    country_flag_filename = Column(String(200))
    country_flag_data = Column(LargeBinary)
