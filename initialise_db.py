"""This scripts sets up inital data for the flights app
"""

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import databases as databases
from databases.base import Base

path_to_config = "./resources/config.json"

with open(path_to_config) as f:
    confg = json.load(f)

engine = create_engine(confg.get("SQLALCHEMY_DATABASE_URI"))

Session = sessionmaker(bind=engine)
session = Session()

# drop all tables first if they are populated
Base.metadata.drop_all(engine)

# Creates all the Tables Model --> DB Table
Base.metadata.create_all(engine)

# create user roles
customers = databases.UserRole(role_name="Customer")
airline_company_representors = databases.UserRole(role_name="Airline")
admins = databases.UserRole(role_name="Admin")

# add user roles first
session.add_all([customers, airline_company_representors, admins])
session.commit()

# create regular users
user01 = databases.User(
    username="user01",
    password="user01",
    email="user01@gmail.com",
    user_role=customers.id,
)


# create admin users
admin01 = databases.User(
    username="admin01",
    password="admin01",
    email="admin01@gmail.com",
    user_role=admins.id,
)
admin02 = databases.User(
    username="admin02",
    password="admin02",
    email="admin02@gmail.com",
    user_role=admins.id,
)


session.add_all(
    [
        user01,
        admin01,
        admin02,
    ]
)
session.commit()


customer01 = databases.Customer(
    firstname="customer01",
    lastname="customer01",
    address="Luxemburger str, Germany",
    phone_no="0782356789",
    credit_card_no="25625256282818",
    user_id=user01.id,
)

session.add(customer01)
session.commit()

admin_01 = databases.Administrator(
    firstname="Jeff", lastname="Willson", user_id=admin01.id
)
admin_02 = databases.Administrator(
    firstname="Ali", lastname="F", user_id=admin02.id
)

session.add_all([admin_01, admin_02])
session.commit()
