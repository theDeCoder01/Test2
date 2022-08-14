import facades.errors as errors
from facades.base import FacadeBase
from facades.login_token import LoginToken
from facades.utils import load_db

session, Base = load_db("./resources/config.json")
User_Roles = Base.classes.User_Roles
Customer = Base.classes.Customer
Country = Base.classes.Country
AirlineCompany = Base.classes.AirlineCompany
Administrator = Base.classes.Administrator


class AdministratorFacade(FacadeBase):
    """The AdministratorFacade class has the highest level of control.
    It provides the following methods: add_country, add_airline, add_customer, add_administrator, remove_country, remove_airline, remove_customer, remove_administrator.


    Parameters
    ----------
    login_token : LoginToken
        The login token of the user.
    """ ""

    def __init__(self, login_token=None) -> None:
        super().__init__()
        self.login_token = login_token

    def __str__(self) -> str:
        return f"AdministratorFacade(login_token='{self.login_token}')"

    @property
    def _user_data(self):
        if self.login_token is None:
            raise errors.InvalidTokenError("Invalid token")

        user_data = LoginToken.decode_auth_token(self.login_token)
        return user_data

    def _get_user_role(self):
        role_id = self._user_data["user_role_id"]
        return session.query(User_Roles).filter_by(id=role_id).first().role_name

    def _validate(self):
        role = self._get_user_role()

        if role != "Admin":
            raise errors.PermissionError(
                "You do not have permission to access this resource"
            )

    def get_all_customers(self):
        # validate user rights
        self._validate()
        all_customers = session.query(Customer).all()
        return all_customers

    def get_all_administrators(self):
        # validate user rights
        self._validate()

        all_administrators = session.query(Administrator).all()
        return all_administrators

    def add_country(self, country_name, country_flag):
        # validate user rights
        self._validate()

        country = Country(
            name=country_name,
            country_flag_filename=country_flag.filename,
            country_flag_data=country_flag.read(),
        )

        try:
            session.add(country)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return country

    def add_airline(self, **kwargs):
        # validate user rights
        self._validate()

        airline = AirlineCompany(**kwargs)

        try:
            session.add(airline)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return airline

    def add_customer(self, **kwargs):
        # validate user rights
        self._validate()

        customer = Customer(**kwargs)

        try:
            session.add(customer)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

        return customer

    def add_administrator(self, **kwargs):
        # validate user rights
        self._validate()

        administrator = Administrator(**kwargs)

        try:
            session.add(administrator)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return administrator

    def remove_country(self, country_id):
        # validate user rights
        self._validate()

        country = session.query(Country).filter_by(id=country_id).first()

        try:
            session.delete(country)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def remove_airline(self, airline_id):
        # validate user rights
        self._validate()

        airline = session.query(AirlineCompany).filter_by(id=airline_id).first()

        try:
            session.delete(airline)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return airline

    def remove_customer(self, customer_id):
        # validate user rights
        self._validate()

        customer = session.query(Customer).filter_by(id=customer_id).first()

        try:
            session.delete(customer)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return customer

    def remove_administrator(self, administrator_id):
        # validate user rights
        self._validate()

        administrator = (
            session.query(Administrator).filter_by(id=administrator_id).first()
        )

        try:
            session.delete(administrator)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return administrator
