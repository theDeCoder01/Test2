import io

from facades import AnonymousFacade, FacadeBase
from facades.functions import (
    generate_user,
    get_airline_by_id,
    get_airline_name_by_id,
    get_country_name_by_id,
    get_user_by_user_id,
    get_user_by_username,
    get_user_role,
    get_user_role_id_by_role_name,
)
from facades.login_token import LoginToken
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from more_itertools import chunked

index_page = Blueprint(
    "index_page",
    __name__,
    template_folder="../templates",
)

facade_base = FacadeBase()

# access the user logo
@index_page.route("/user-photo/<user_id>")
def server_user_photo(user_id):
    user_id = int(user_id)
    user = get_user_by_user_id(user_id)
    file_ext = user.photo_filename.split(".")[1]
    return send_file(io.BytesIO(user.photo_data), mimetype=f"image/{file_ext}")


# access the country flag logo
@index_page.route("/country-photo/<country_id>")
def serve_country_flag_image(country_id):
    country_id = int(country_id)
    country = facade_base.get_country_by_id(country_id)
    file_ext = country.country_flag_filename.split(".")[1]
    return send_file(
        io.BytesIO(country.country_flag_data), mimetype=f"image/{file_ext}"
    )


# for anonymous users
@index_page.route("/")
def index():
    login_token = session.get("login_token")
    user = None

    if login_token:
        current_user_role = get_user_role(login_token)
        user_data = LoginToken.decode_auth_token(login_token)
        user = get_user_by_username(user_data["username"])
    else:
        current_user_role = None
    flights = FacadeBase().get_all_flights()
    flights = chunked(flights, 4)
    return render_template(
        "index.html",
        current_user_role=current_user_role,
        flights=flights,
        get_airline_name_by_id=get_airline_name_by_id,
        get_country_name_by_id=get_country_name_by_id,
        get_airline_by_id=get_airline_by_id,
        get_user_by_user_id=get_user_by_user_id,
        user=user,
    )


# allow existing users to login
@index_page.route("/login", methods=["GET", "POST"])
def login():
    error = request.values.get("error")

    if request.method == "POST":
        username = request.values.get("username")
        password = request.values.get("password")

        login_token = AnonymousFacade().login(username, password)

        if login_token is None:
            return render_template("login.html", error="Invalid username or password")

        _, user_role = generate_user(login_token)

        session["login_token"] = login_token

        urls = {
            "Customer": redirect(url_for("customer_page.portal")),
            "Airline": redirect(url_for("airline_company_page.portal")),
            "Admin": redirect(url_for("admin_page.portal")),
        }
        return urls[user_role]

    return render_template("login.html", error=error)


# route to allow new users to register
@index_page.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
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
        user = facade_base.create_new_user(
            username=username,
            password=password,
            email=email,
            user_role=user_role_id,
            photo_filename=customer_photo.filename if customer_photo else None,
            photo_data=customer_photo.read() if customer_photo else None,
        )

        # then create the customer
        facade_base.add_customer(
            firstname=firstname,
            lastname=lastname,
            address=address,
            phone_no=phone_no,
            credit_card_no=credit_card_no,
            user_id=user.id,
        )
        return redirect(url_for("index_page.login"))

    return render_template("register.html")


# end user session
@index_page.route("/logout", methods=["GET", "POST"])
def logout():
    # remove the login_token from the session and redirect to the login page
    session.pop("login_token", None)
    return redirect(url_for("index_page.login"))
