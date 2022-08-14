from sqlalchemy import BigInteger, Column, ForeignKey, String

from databases.base import Base


class Customer(Base):
    __tablename__ = "Customer"
    id = Column(BigInteger, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_no = Column(String, unique=True)
    credit_card_no = Column(String, unique=True)
    user_id = Column(BigInteger, ForeignKey("User.id"), nullable=False)
