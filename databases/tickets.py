from sqlalchemy import BigInteger, Column, ForeignKey

from databases.base import Base


class Ticket(Base):
    __tablename__ = "Ticket"
    id = Column(BigInteger, primary_key=True)
    flight_id = Column(BigInteger, ForeignKey("Flight.id"), unique=True)
    customer_id = Column(BigInteger, ForeignKey("Customer.id"), unique=True)
    