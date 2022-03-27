from functools import wraps

import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from quart import current_app, request

from basicauth.helpers.excecptions import Unauthorized


def protected(view):
    """Checks header for Authorization with access token"""

    @wraps(view)
    async def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise Unauthorized

        authotization = request.headers["Authorization"]
        try:
            token = authotization.split(" ")[1]
        except IndexError:
            raise Unauthorized

        try:
            jwt.decode(
                token,
                current_app.config["TOKEN_SECRET"],
                algorithms=[
                    "HS256",
                ],
            )
        except (InvalidSignatureError, ExpiredSignatureError):
            return Unauthorized

        return await view(*args, **kwargs)

    return wrapper
