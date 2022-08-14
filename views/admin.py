from facades import AdministratorFacade, FacadeBase
from facades.functions import (
    get_country_name_by_id,
    get_user_by_user_id,
    get_user_by_username,
    get_user_role,
    get_user_role_id_by_role_name,
)
from flask import Blueprint, redirect, render_template, request, session, url_for

admin_page = Blueprint("admin_page", __name__, template_folder="../templates")

facade_base = FacadeBase()


@admin_page.route("/portal", methods=["GET", "POST"])
def portal():
    login_token = session.get("login_token")
    countries = facade_base.get_all_countries()
    airlines = None
    administrators = None
    customers = None

    if login_token:
        current_user_role = get_user_role(login_token)
        admin_facade = AdministratorFacade(login_token=login_token)
        airlines = admin_facade.get_all_airlines()
        administrators = admin_facade.get_all_administrators()
        customers = admin_facade.get_all_customers()
        current_logged_in_admin = admin_facade._user_data["id"]
        user = get_user_by_username(admin_facade._user_data["username"])
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )
    return render_template(
        "admin_portal.html",
        current_user_role=current_user_role,
        countries=countries,
        airlines=airlines,
        administrators=administrators,
        customers=customers,
        user=user,
        get_user_by_user_id=get_user_by_user_id,
        current_logged_in_admin=current_logged_in_admin,
        get_country_name_by_id=get_country_name_by_id,
    )


# add route for adding a new country
@admin_page.route("/add-country", methods=["POST"])
def add_country():
    login_token = session.get("login_token")
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)
        country_name = request.form.get("name")
        country_flag = request.files.get("country-flag")

        admin_facade.add_country(country_name, country_flag)
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for adding a new airline
@admin_page.route("/add-airline", methods=["POST"])
def add_airline():
    login_token = session.get("login_token")
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)
        airline_name = request.form.get("name")
        airline_country_id = request.form.get("country_id")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        airline_logo = request.files.get("airline-logo")
        user_role_id = get_user_role_id_by_role_name("Airline")

        # create the user first
        user = admin_facade.create_new_user(
            username=username,
            password=password,
            email=email,
            user_role=user_role_id,
            photo_filename=airline_logo.filename if airline_logo else None,
            photo_data=airline_logo.read() if airline_logo else None,
        )

        # then create the airline
        admin_facade.add_airline(
            name=airline_name, country_id=airline_country_id, user_id=user.id
        )
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for adding a new administrator
@admin_page.route("/add-administrator", methods=["POST"])
def add_admin():
    login_token = session.get("login_token")
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)
        firstname = request.form.get("admin-firstname")
        lastname = request.form.get("admin-lastname")
        admin_photo = request.files.get("admin-photo")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        user_role_id = get_user_role_id_by_role_name("Administrator")

        # create the user first
        user = admin_facade.create_new_user(
            username=username,
            password=password,
            email=email,
            user_role=user_role_id,
            photo_filename=admin_photo.filename if admin_photo else None,
            photo_data=admin_photo.read() if admin_photo else None,
        )

        # then create the administrator
        admin_facade.add_administrator(
            firstname=firstname, lastname=lastname, user_id=user.id
        )
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for adding a new customer
@admin_page.route("/add-customer", methods=["POST"])
def add_customer():
    login_token = session.get("login_token")
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        address = request.form.get("address")
        customer_photo = request.files.get("customer-photo")
        phone_no = request.form.get("customer-phone-no")
        credit_card_no = request.form.get("credit_card_no")

        user_role_id = get_user_role_id_by_role_name("Customer")

        # create the user first
        user = admin_facade.create_new_user(
            username=username,
            password=password,
            email=email,
            user_role=user_role_id,
            photo_filename=customer_photo.filename if customer_photo else None,
            photo_data=customer_photo.read() if customer_photo else None,
        )

        # then create the airline
        admin_facade.add_customer(
            firstname=firstname,
            lastname=lastname,
            address=address,
            phone_no=phone_no,
            credit_card_no=credit_card_no,
            user_id=user.id,
        )
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for removing a country
@admin_page.route("/remove-country")
def remove_country():
    login_token = session.get("login_token")
    country_id = int(request.values.get("country_id"))
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)

        admin_facade.remove_country(country_id)
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for removing an airline
@admin_page.route("/remove-airline")
def remove_airline():
    login_token = session.get("login_token")
    airline_id = int(request.values.get("airline_id"))
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)

        admin_facade.remove_airline(airline_id)
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for removing a customer
@admin_page.route("/remove-customer")
def remove_customer():
    login_token = session.get("login_token")
    customer_id = int(request.values.get("customer_id"))
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)

        admin_facade.remove_customer(customer_id)
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )


# add route for removing an administrator
@admin_page.route("/remove-administrator")
def remove_admin():
    login_token = session.get("login_token")
    admin_id = int(request.values.get("admin_id"))
    admin_facade = None

    if login_token:
        admin_facade = AdministratorFacade(login_token=login_token)

        admin_facade.remove_administrator(admin_id)
        return redirect(url_for("admin_page.portal"))
    else:
        error = "You must be logged in to perform this operation"
        return redirect(
            url_for(
                "index_page.login",
                error=error,
            )
        )
