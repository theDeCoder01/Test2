from facades import AirlineFacade, FacadeBase
from facades.functions import (
    get_airline_by_user_id,
    get_airline_name_by_id,
    get_country_name_by_id,
    get_flight_by_id,
    get_user_by_username,
    get_user_role,
    get_user_role_id_by_role_name,
)
from flask import Blueprint, redirect, render_template, request, session, url_for

airline_company_page = Blueprint(
    "airline_company_page", __name__, template_folder="../templates"
)

facade_base = FacadeBase()

# add route to register a new airline company
@airline_company_page.route("/register", methods=["POST"])
def register():
    airline_name = request.form.get("name")
    airline_country_id = request.form.get("country_id")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    airline_logo = request.files.get("airline-logo")
    user_role_id = get_user_role_id_by_role_name("Airline")

    # create the user first
    user = facade_base.create_new_user(
        username=username,
        password=password,
        email=email,
        user_role=user_role_id,
        photo_filename=airline_logo.filename if airline_logo else None,
        photo_data=airline_logo.read() if airline_logo else None,
    )

    # then create the airline
    facade_base.add_airline(
        name=airline_name, country_id=airline_country_id, user_id=user.id
    )
    return redirect(url_for("index_page.login"))


# allow users to view airline profile
@airline_company_page.route("/profile", methods=["GET", "POST"])
def profile():
    login_token = session.get("login_token")
    airline_facade = None
    user = None
    countries = FacadeBase().get_all_countries()
    user_update_msg = request.values.get("user_update_msg")

    if login_token:
        current_user_role = get_user_role(login_token)
        airline_facade = AirlineFacade(login_token)
        user = get_user_by_username(airline_facade._user_data["username"])
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )
    return render_template(
        "airline_profile.html",
        current_user_role=current_user_role,
        airline_facade=airline_facade,
        user=user,
        user_update_msg=user_update_msg,
        countries=countries,
        get_airline_by_user_id=get_airline_by_user_id,
        get_country_name_by_id=get_country_name_by_id,
    )


# allow users to update the users table
@airline_company_page.route("/update-profile", methods=["POST"])
def update_profile():
    login_token = session.get("login_token")
    airline_facade = None

    if login_token:
        airline_facade = AirlineFacade(login_token)
        email = request.form.get("email")
        password = request.form.get("password")
        photo = request.files.get("photo")

        airline_facade.update_user_profile(email, password, photo)
        user_update_msg = "User profile updated successfully"
        return redirect(
            url_for("airline_company_page.profile", user_update_msg=user_update_msg)
        )
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# allow users to update the customers table
@airline_company_page.route("/update-profile-data", methods=["POST"])
def update_profile_data():
    login_token = session.get("login_token")

    if login_token:
        airline_facade = AirlineFacade(login_token)
        name = request.form.get("name")
        country_id = request.form.get("country_id")
        airline_id = get_airline_by_user_id(airline_facade._user_data["id"]).id

        airline_facade.update_airline(airline_id, name, country_id)
        return redirect(url_for("airline_company_page.profile"))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


@airline_company_page.route("/portal", methods=["GET", "POST"])
def portal():
    login_token = session.get("login_token")
    user = None
    flights = None
    countries = facade_base.get_all_countries()

    if login_token:
        current_user_role = get_user_role(login_token)
        airline_facade = AirlineFacade(login_token)
        flights = airline_facade.get_my_flights()
        user = get_user_by_username(airline_facade._user_data["username"])
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )
    return render_template(
        "airline_portal.html",
        current_user_role=current_user_role,
        user=user,
        flights=flights,
        get_flight_by_id=get_flight_by_id,
        get_airline_name_by_id=get_airline_name_by_id,
        get_country_name_by_id=get_country_name_by_id,
        countries=countries,
    )


# route to update flight
@airline_company_page.route("/update-flight", methods=["GET", "POST"])
def update_flight():
    login_token = session.get("login_token")
    flight_id = request.values.get("flight_id")
    origin_country_id = request.form.get("origin_country_id")
    destination_country_id = request.form.get("destination_country_id")
    departure_date = request.form.get("departure_date")
    landing_date = request.form.get("landing_date")
    remaining_tickets = request.form.get("remaining_tickets")

    if login_token:
        airline_facade = AirlineFacade(login_token)
        airline_facade.update_flight(
            flight_id,
            origin_country_id,
            destination_country_id,
            departure_date,
            landing_date,
            remaining_tickets,
        )
        return redirect(url_for("airline_company_page.portal"))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# route to add flight
@airline_company_page.route("/add-flight", methods=["GET", "POST"])
def add_flight():
    login_token = session.get("login_token")
    origin_country_id = request.form.get("origin_country_id")
    destination_country_id = request.form.get("destination_country_id")
    departure_date = request.form.get("departure_date")
    landing_date = request.form.get("landing_date")
    remaining_tickets = request.form.get("remaining_tickets")

    if login_token:

        airline_facade = AirlineFacade(login_token)
        airline_facade.add_flight(
            origin_country_id=origin_country_id,
            destination_country_id=destination_country_id,
            departure_date=departure_date,
            landing_date=landing_date,
            remaining_tickets=int(remaining_tickets),
            airline_company_id=get_airline_by_user_id(
                airline_facade._user_data["id"]
            ).id,
        )
        return redirect(url_for("airline_company_page.portal"))

    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# route to remove a flight from the airline's account
@airline_company_page.route("/remove-flight")
def remove_flight():
    login_token = session.get("login_token")
    flight_id = request.args.get("flight_id")

    if login_token:
        airline_facade = AirlineFacade(login_token)
        flight = get_flight_by_id(flight_id)
        airline_facade.remove_flight(flight)
        return redirect(url_for("airline_company_page.portal"))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )
