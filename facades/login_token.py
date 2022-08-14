import jwt

import facades.errors as errors
from facades.utils import load_config

confg = load_config("./resources/config.json")


class LoginToken:
    def __init__(self, user):
        self.user = user

    def encode_auth_token(self):
        """It takes a user object, and returns a JWT token

        Returns
        -------
            The token is being returned.

        """
        try:
            payload = {
                "id": self.user.id,
                "username": self.user.username,
                "user_role_id": self.user.user_role,
            }
            return jwt.encode(payload, confg.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """It takes a token as an argument and returns the payload of the token if the token is valid

        Parameters
        ----------
        auth_token
            The token that needs to be decoded.

        Returns
        -------
            The payload is being returned.

        """
        try:
            payload = jwt.decode(
                auth_token, confg.get("SECRET_KEY"), algorithms="HS256"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise errors.ExpiredTokenError("Signature expired. Please log in again.")

        except jwt.InvalidTokenError:
            raise errors.InvalidTokenError("Invalid token. Please log in again.")
