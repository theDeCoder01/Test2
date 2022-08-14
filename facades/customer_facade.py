import sqlalchemy.exc

import facades.errors as errors
from facades.base import FacadeBase
from facades.login_token import LoginToken
from facades.utils import load_db

session, Base = load_db("./resources/config.json")

# Required tables for the CustomerFacade:
User = Base.classes.User
Customer = Base.classes.Customer
Flight = Base.classes.Flight
Ticket = Base.classes.Ticket


class CustomerFacade(FacadeBase):
    """Sets the stage for a given customer when using the flight system application
    - The customer will be required to authenticate before using the application with the LoginToken
    - The customer will be required to register before using the application with the LoginToken

    Parameters
    ----------
    login_token : str
        The Login Token of the customer
        
    Examples
    --------
    >>> customer_facade = CustomerFacade(login_token)
    >>> customer_facade.update_customer(firstname="Jeff", lastname="Wills", address="53 Abbey court, UK", phone_no='1828292929', credit_card_no='0189191717171')

    """ ""

    def __init__(self, login_token=None) -> None:
        super().__init__()
        self.login_token = login_token

    def __str__(self) -> str:
        return f"CustomerFacade(login_token = '{self.login_token}')"

    @property
    def _user_data(self):
        if self.login_token is None:
            raise errors.InvalidTokenError("Invalid token")

        user_data = LoginToken.decode_auth_token(self.login_token)
        return user_data

    def _validate_customer(self, customer):
        if self._user_data["id"] != customer.user_id:
            raise errors.InvalidCredentialsError("invalid credentials")

    def _validate(self):
        customer = (
            session.query(Customer).filter_by(user_id=self._user_data["id"]).first()
        )
        if self._user_data["id"] != customer.user_id:
            raise errors.InvalidCredentialsError("invalid credentials")

    def update_user_profile(self, email, password, photo=None):
        try:
            session.query(User).filter_by(id=self._user_data["id"]).update(
                {
                    "email": email,
                    "password": password,
                    "photo_filename": photo.filename if photo else None,
                    "photo_data": photo.read() if photo else None,
                }
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def update_customer(self, firstname, lastname, address, phone_no, credit_card_no):
        # cross-check the received token before performing any operation that the item belongs to the user
        customer = session.query(Customer).filter_by(phone_no=phone_no).first()
        self._validate_customer(customer)

        try:
            session.query(Customer).filter_by(user_id=self._user_data["id"]).update(
                {
                    "firstname": firstname,
                    "lastname": lastname,
                    "address": address,
                    "phone_no": phone_no,
                    "credit_card_no": credit_card_no,
                }
            )
            session.commit()
        except:
            session.rollback()

        return customer

    def add_ticket(self, **kwargs):
        try:
            # add the ticket to the database
            ticket = Ticket(**kwargs)
            session.add(ticket)
            # decrease the remaaining_tickets from the flight
            flight = session.query(Flight).filter_by(id=ticket.flight_id).first()
            flight.remaining_tickets -= 1
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def remove_ticket(self, ticket):
        # validate user before removing any ticket
        customer = session.query(Customer).filter_by(id=ticket.customer_id).first()
        self._validate_customer(customer)

        try:
            # remove the ticket from the database
            session.delete(ticket)
            # increase the remaaining_tickets from the flight
            flight = session.query(Flight).filter_by(id=ticket.flight_id).first()
            flight.remaining_tickets += 1

            session.commit()

        except sqlalchemy.exc.InvalidRequestError:
            current_db_sessions = session.object_session(ticket)
            current_db_sessions.delete(ticket)
            # increase the remaaining_tickets from the flight
            flight = (
                current_db_sessions.query(Flight).filter_by(id=ticket.flight_id).first()
            )
            flight.remaining_tickets += 1
            current_db_sessions.commit()

        except Exception as e:
            session.rollback()
            raise e

    def get_my_tickets(self):
        customer = (
            session.query(Customer).filter_by(user_id=self._user_data["id"]).first()
        )

        return session.query(Ticket).filter_by(customer_id=customer.id).all()
