import sqlalchemy.exc

import facades.errors as errors
from facades.base import FacadeBase
from facades.login_token import LoginToken
from facades.utils import load_db
from facades.validation import validate_flight

session, Base = load_db("./resources/config.json")

# Required tables for the AirlineFacade:
AirlineCompany = Base.classes.AirlineCompany
Flight = Base.classes.Flight
Ticket = Base.classes.Ticket
User = Base.classes.User


class AirlineFacade(FacadeBase):
    def __init__(self, login_token=None) -> None:
        super().__init__()
        self.login_token = login_token

    def __str__(self) -> str:
        return f"AirlineFacade(login_token='{self.login_token}')"

    @property
    def _user_data(self):
        if self.login_token is None:
            raise errors.InvalidTokenError("Invalid token")

        user_data = LoginToken.decode_auth_token(self.login_token)
        return user_data

    def _validate_flight(self, flight):
        airline_company = (
            session.query(AirlineCompany)
            .filter_by(user_id=self._user_data["id"])
            .first()
        )

        if airline_company.id != flight.airline_company_id:
            raise errors.PermissionError(
                "You are not allowed to remove flights from this airline"
            )

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

    def update_airline(self, airline_id, name, country_id):
        airline = session.query(AirlineCompany).filter_by(id=airline_id).first()

        # cross-check the received token before performing any operation that the item belongs to the user
        if self._user_data["id"] != airline.user_id:
            raise errors.PermissionError("You are not allowed to update this airline")

        try:
            session.query(AirlineCompany).filter_by(
                user_id=self._user_data["id"]
            ).update(
                {
                    "name": name,
                    "country_id": country_id,
                }
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return airline

    def update_flight(
        self,
        flight_id,
        origin_country_id,
        destination_country_id,
        departure_date,
        landing_date,
        remaining_tickets,
    ):
        # get the airline company from the flight
        # validate the airline company before updating the flight
        flight = session.query(Flight).filter_by(id=flight_id).first()
        self._validate_flight(flight)

        # validate flight parameters
        validate_flight(flight)

        try:
            session.query(Flight).filter_by(id=flight.id).update(
                {
                    "departure_date": departure_date,
                    "origin_country_id": origin_country_id,
                    "destination_country_id": destination_country_id,
                    "landing_date": landing_date,
                    "remaining_tickets": int(remaining_tickets),
                }
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return flight

    def add_flight(self, **kwargs):
        # get the airline company from the flight
        # validate the airline company before adding the flight
        flight = Flight(**kwargs)
        self._validate_flight(flight)

        # validate flight parameters
        validate_flight(flight)

        try:
            session.add(flight)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def remove_flight(self, flight):
        # get the airline company from the flight
        # validate the airline company before removing the flight
        self._validate_flight(flight)
        try:
            session.delete(flight)
            session.commit()

        except sqlalchemy.exc.InvalidRequestError:
            current_db_sessions = session.object_session(flight)
            current_db_sessions.delete(flight)
            current_db_sessions.commit()

        except Exception as e:
            session.rollback()
            raise e

    def get_my_flights(self):
        airline_company = (
            session.query(AirlineCompany)
            .filter_by(user_id=self._user_data["id"])
            .first()
        )

        return (
            session.query(Flight).filter_by(airline_company_id=airline_company.id).all()
        )
