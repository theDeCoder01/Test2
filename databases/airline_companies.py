from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from databases.base import Base


class AirlineCompany(Base):
    __tablename__ = "AirlineCompany"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("Country.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("User.id"), nullable=False)
    