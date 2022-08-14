from facades.administrator_facade import AdministratorFacade
from facades.airline_facade import AirlineFacade
from facades.customer_facade import CustomerFacade
from facades.login_token import LoginToken
from facades.utils import load_db

session, Base = load_db("./resources/config.json")

# Required tables for the FacadeBase:
User_Roles = Base.classes.User_Roles
User = Base.classes.User
AirlineCompany = Base.classes.AirlineCompany
Country = Base.classes.Country
Flight = Base.classes.Flight
Ticket = Base.classes.Ticket
Customer = Base.classes.Customer


def get_user_role_id_by_role_name(role_name):
    user_role = session.query(User_Roles).filter_by(role_name=role_name).first()
    return user_role.id


def get_airline_name_by_id(airline_company_id):
    airline = (
        session.query(AirlineCompany)
        .filter(AirlineCompany.id == airline_company_id)
        .first()
    )
    return airline.name


def get_airline_by_id(airline_id):
    airline = (
        session.query(AirlineCompany).filter(AirlineCompany.id == airline_id).first()
    )
    return airline


def get_user_by_username(username):
    user = session.query(User).filter(User.username == username).first()
    return user


def get_customer_by_user_id(user_id):
    customer = session.query(Customer).filter(Customer.user_id == user_id).first()
    return customer


def get_airline_by_user_id(user_id):
    airline = (
        session.query(AirlineCompany).filter(AirlineCompany.user_id == user_id).first()
    )
    return airline


def get_user_by_user_id(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def get_ticket_by_id(ticket_id):
    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    return ticket


def get_ticket_by_flight_id(flight_id):
    ticket = session.query(Ticket).filter(Ticket.flight_id == flight_id).first()
    return ticket


def get_flight_by_id(flight_id):
    flight = session.query(Flight).filter(Flight.id == flight_id).first()
    return flight


def get_country_name_by_id(country_id):
    country = session.query(Country).filter(Country.id == country_id).first()
    return country.name


def get_user_role(login_token):
    user_data = LoginToken.decode_auth_token(login_token)
    role_id = user_data["user_role_id"]
    role = session.query(User_Roles).filter_by(id=role_id).first().role_name
    return role


def get_user_role_by_user_role_id(user_role_id):
    user_role = session.query(User_Roles).filter_by(id=user_role_id).first()
    return user_role.role_name


def generate_user(login_token):
    user_data = LoginToken.decode_auth_token(login_token)
    role_id = user_data["user_role_id"]
    role = session.query(User_Roles).filter_by(id=role_id).first().role_name
    roles = {
        "Customer": CustomerFacade(login_token=login_token),
        "Airline": AirlineFacade(login_token=login_token),
        "Admin": AdministratorFacade(login_token=login_token),
    }
    return roles[role], role
