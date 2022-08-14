from facades import CustomerFacade, FacadeBase
from facades.functions import (
    get_airline_by_id,
    get_airline_name_by_id,
    get_country_name_by_id,
    get_customer_by_user_id,
    get_flight_by_id,
    get_ticket_by_id,
    get_user_by_user_id,
    get_user_by_username,
    get_user_role,
)
from flask import Blueprint, redirect, render_template, request, session, url_for
from more_itertools import chunked

customer_page = Blueprint(
    "customer_page",
    __name__,
    template_folder="../templates",
    static_folder="static",
)


# allow users to view their profile
@customer_page.route("/profile", methods=["GET", "POST"])
def profile():
    login_token = session.get("login_token")
    customer_facade = None
    user = None
    user_update_msg = request.values.get("user_update_msg")

    if login_token:
        current_user_role = get_user_role(login_token)
        customer_facade = CustomerFacade(login_token)
        user = get_user_by_username(customer_facade._user_data["username"])
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )
    return render_template(
        "customer_profile.html",
        current_user_role=current_user_role,
        customer_facade=customer_facade,
        user=user,
        get_customer_by_user_id=get_customer_by_user_id,
        user_update_msg=user_update_msg,
    )


# allow users to update the users table
@customer_page.route("/update-profile", methods=["POST"])
def update_profile():
    login_token = session.get("login_token")

    if login_token:
        customer_facade = CustomerFacade(login_token)
        email = request.form.get("email")
        password = request.form.get("password")
        photo = request.files.get("photo")

        customer_facade.update_user_profile(email, password, photo)
        user_update_msg = "User profile updated successfully"
        return redirect(
            url_for("customer_page.profile", user_update_msg=user_update_msg)
        )
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# allow users to update the customers table
@customer_page.route("/update-profile-data", methods=["POST"])
def update_profile_data():
    login_token = session.get("login_token")

    if login_token:
        customer_facade = CustomerFacade(login_token)
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        address = request.form.get("address")
        phone_no = request.form.get("phone_no")
        credit_card_no = request.form.get("credit_card_no")

        customer_facade.update_customer(
            firstname, lastname, address, phone_no, credit_card_no
        )
        return redirect(url_for("customer_page.profile"))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# show users dashboard/ portal
@customer_page.route("/portal", methods=["GET", "POST"])
def portal():
    login_token = session.get("login_token")
    customer_facade = None
    flights = FacadeBase().get_all_flights()
    flights = chunked(flights, 4)
    tickets = None
    user = None
    ticket_error = request.values.get("ticket_error")

    if login_token:
        current_user_role = get_user_role(login_token)
        customer_facade = CustomerFacade(login_token)
        user = get_user_by_username(customer_facade._user_data["username"])
        tickets = customer_facade.get_my_tickets()
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )
    return render_template(
        "customer_portal.html",
        current_user_role=current_user_role,
        tickets=tickets,
        customer_facade=customer_facade,
        get_flight_by_id=get_flight_by_id,
        get_airline_name_by_id=get_airline_name_by_id,
        get_country_name_by_id=get_country_name_by_id,
        get_airline_by_id=get_airline_by_id,
        get_user_by_user_id=get_user_by_user_id,
        flights=flights,
        ticket_error=ticket_error,
        user=user,
    )


# remove ticket from user's account
@customer_page.route("/remove-ticket")
def remove_ticket():
    login_token = session.get("login_token")
    if login_token:
        customer_facade = CustomerFacade(login_token)
        ticket_id = request.args.get("ticket_id")
        ticket = get_ticket_by_id(ticket_id)
        customer_facade.remove_ticket(ticket)
        return redirect(url_for("customer_page.portal"))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )


# add ticket to user's account
@customer_page.route("/add-ticket")
def add_ticket():
    login_token = session.get("login_token")
    if login_token:
        ticket_error = None
        customer_facade = CustomerFacade(login_token)
        flight_id = request.args.get("flight_id")
        try:
            customer_facade.add_ticket(
                flight_id=flight_id, customer_id=customer_facade._user_data["id"]
            )
            return redirect(url_for("customer_page.portal"))
        except:
            ticket_error = "You already have a ticket for this flight"
            return redirect(url_for("customer_page.portal", ticket_error=ticket_error))
    else:
        return redirect(
            url_for(
                "index_page.login",
                error="You must be logged in to perform this operation",
            )
        )
