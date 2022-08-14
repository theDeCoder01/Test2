from sqlalchemy import BigInteger, Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from databases.base import Base


class UserRole(Base):
    __tablename__ = "User_Roles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(250), unique=True)
    users = relationship("User", backref="User_Roles", lazy=True)


class User(Base):
    __tablename__ = "User"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(250), unique=True)
    password = Column(String, primary_key=False, unique=False, nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    user_role = Column(Integer, ForeignKey("User_Roles.id"), nullable=False)
    photo_filename = Column(String(200))
    photo_data = Column(LargeBinary)

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        user_role: int,
        photo_filename=None,
        photo_data=None,
    ):
        self.username = username
        self.password = password
        self.email = email
        self.user_role = user_role
        self.photo_filename = photo_filename
        self.photo_data = photo_data

    def __repr__(self) -> str:
        return "<User {}, role_id: {}>".format(self.username, self.user_role)
