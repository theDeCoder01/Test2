import datetime
import re

import facades.errors as errors


def validate_flight(flight) -> None:
    # if remaining_tickets is negative, raise an error
    if flight.remaining_tickets < 0:
        raise errors.InvalidParametersError("remaining_tickets cannot be negative")

    # if landing_date is before departure_date, raise an error
    if flight.landing_date < flight.departure_date:
        raise errors.InvalidParametersError(
            "landing_date cannot be before departure_date"
        )

    # if departure_date is in the past, raise an error
    if isinstance(flight.departure_date, datetime.datetime):
        departure_date = flight.departure_date.strftime("%Y-%m-%d %H:%M:%S")
        landing_date = flight.landing_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        departure_date = flight.departure_date
        landing_date = flight.landing_date

    if departure_date < datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        raise errors.InvalidParametersError("departure_date cannot be in the past")

    # if landing_date is in the past, raise an error
    if landing_date < datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        raise errors.InvalidParametersError("landing_date cannot be in the past")

    # if origin_country_id is the same with the destination_country_id, raise an error
    if flight.origin_country_id == flight.destination_country_id:
        raise errors.InvalidParametersError(
            "origin_country_id cannot be the same with destination_country_id"
        )


def validate_new_user(user) -> None:
    # if password is less than 6 characters, raise an error
    if len(user.password) < 6:
        raise errors.InvalidParametersError("password must be at least 6 characters")

    # if username is less than 3 characters, raise an error
    if len(user.username) < 3:
        raise errors.InvalidParametersError("username must be at least 3 characters")

    # validate email address is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise errors.InvalidParametersError("email address is not valid")
