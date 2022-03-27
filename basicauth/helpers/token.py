import datetime

import jwt
from quart import current_app


def get_token(payload):
    user = payload
    try:
        user.pop("exp")
    except KeyError:
        pass

    access_data = refresh_data = user.copy()

    accessTokenExpires = datetime.datetime.now() + datetime.timedelta(days=1)
    refreshTokenExpires = datetime.datetime.now() + datetime.timedelta(days=30)

    access_data["exp"] = accessTokenExpires
    refresh_data["exp"] = refreshTokenExpires

    access_token = jwt.encode(access_data, current_app.config["TOKEN_SECRET"])
    refresh_token = jwt.encode(refresh_data, current_app.config["REFRESH_SECRET"])

    token = {
        "accessToken": access_token,
        "accessTokenExpires": accessTokenExpires,
        "refreshToken": refresh_token,
        "refreshTokenExpires": refreshTokenExpires,
    }

    return {"user": user, "token": token}
