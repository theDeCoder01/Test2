from facades.utils import load_db
from facades.validation import validate_new_user

session, Base = load_db("./resources/config.json")

# Required tables for the FacadeBase:
User = Base.classes.User
AirlineCompany = Base.classes.AirlineCompany
Flight = Base.classes.Flight
Country = Base.classes.Country
Customer = Base.classes.Customer

    

class FacadeBase:
    """The FacadeBase class is the base class for all facades.
    It sets the stage for all types of users that will use the flight system
    """    ""
    
    def get_all_flights(self):
        return session.query(Flight).all()
    
    def get_flight_by_id(self, id):
        return session.query(Flight).filter_by(id=id).first()
    
    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        return session.query(Flight).filter_by(origin_country_id=origin_country_id, destination_country_id=destination_country_id, date=date).all()
        
    def get_all_airlines(self):
        return session.query(AirlineCompany).all()
    
    def get_airline_by_id(self, id):
        return session.query(AirlineCompany).filter_by(id=id).first()
    
    def get_airline_by_parameters(self, **kwargs):
        return session.query(AirlineCompany).filter_by(**kwargs).first()
    
    def get_all_countries(self):
        return session.query(Country).all()
    
    def get_country_by_id(self, id):
        return session.query(Country).filter_by(id=id).first()
    
    def create_new_user (self, **kwargs):
        user = User(**kwargs)
        validate_new_user(user)
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return user
    
    def add_customer(self, **kwargs):
        customer = Customer(**kwargs)
        try:
            session.add(customer)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return customer
    
    def add_airline(self, **kwargs):
        airline = AirlineCompany(**kwargs)
        try:
            session.add(airline)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return airline
        