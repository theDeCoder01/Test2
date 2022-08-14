from flask import Flask

from facades.utils import load_config
from views.admin import admin_page
from views.airline import airline_company_page
from views.customer import customer_page
from views.index import index_page

app = Flask(__name__)
config = load_config()
app.config["SECRET_KEY"] = config.get("SECRET_KEY")

app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(customer_page, url_prefix="/customer")
app.register_blueprint(airline_company_page, url_prefix="/airline-comapny")
app.register_blueprint(admin_page, url_prefix="/admin")


if __name__ == "__main__":
    app.run(debug=True)
