from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer

from databases.base import Base


class Flight(Base):
    __tablename__ = "Flight"
    id = Column(Integer, primary_key=True)
    airline_company_id = Column(
        BigInteger, ForeignKey("AirlineCompany.id"), nullable=False
    )
    origin_country_id = Column(Integer, ForeignKey("Country.id"), nullable=False)
    destination_country_id = Column(Integer, ForeignKey("Country.id"), nullable=False)
    departure_date = Column(DateTime, nullable=False)
    landing_date = Column(DateTime, nullable=False)
    remaining_tickets = Column(Integer, nullable=False)
