import pytest

import facades
import facades.errors as errors
from facades.functions import get_user_role_id_by_role_name
from facades.utils import load_db


def test_create_new_customer():
    user_role_id = get_user_role_id_by_role_name("Customer")

    assert user_role_id == 1, "The user role id should be 1"

    user = facades.FacadeBase().create_new_user(
        username="some_username",
        password="password",
        email="some_email@gmail.com",
        user_role=user_role_id,
    )

    assert user is not None, "The user should not be None"

    customer = facades.AnonymousFacade().add_customer(
        firstname="firstname",
        lastname="lastname",
        address="address",
        phone_no="1234056789",
        credit_card_no="17189303232282",
        user_id=user.id,
    )
    assert customer is not None, "The customer should not be None"


def test_login_user():
    login_token = facades.AnonymousFacade().login("user01", "user01")
    assert (
        login_token is not None
    ), "The login token should not be None because the user exists"

    customer = facades.CustomerFacade(login_token)
    all_customers = customer.get_my_tickets()
    assert all_customers is not None, "It should return the customer's tickets"


def test_raise_error_for_user():
    with pytest.raises(errors.InvalidParametersError):
        user = facades.FacadeBase().create_new_user(
            username="asd",
            password="hhj",
            email="hjgmail.com",
            user_role=1,
        )
