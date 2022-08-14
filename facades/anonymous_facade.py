from typing import Union

from facades.base import FacadeBase
from facades.login_token import LoginToken
from facades.utils import load_db

session, Base = load_db("./resources/config.json")

# Required tables for the AnonymousFacade:
User = Base.classes.User
Customer = Base.classes.Customer


class AnonymousFacade(FacadeBase):
    """The AnonymousFacade class used for users just visiting the flight system.
    The user has the option to register as a customer or to login.  

    """ ""

    def login(self, username: str, password: str) -> Union[str, Exception, None]:
        user = (
            session.query(User).filter_by(username=username, password=password).first()
        )
        if user:
            login_token = LoginToken(user).encode_auth_token()
            return login_token
        return None

    def add_customer(self, **kwargs):
        try:
            customer = Customer(**kwargs)
            session.add(customer)
            session.commit()

        except Exception as e:
            print(e)
            session.rollback()
            raise e

        return customer
