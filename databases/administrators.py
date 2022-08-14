from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from databases.base import Base


class Administrator(Base):
    __tablename__ = "Administrator"
    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey("User.id"), nullable=False)
    