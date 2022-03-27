import json

import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from quart import current_app, request
from werkzeug.security import check_password_hash, generate_password_hash

from basicauth.helpers.decorators import protected
from basicauth.helpers.token import get_token


async def authorize():
    try:
        body = json.loads(await request.data)
    except json.JSONDecodeError:
        return {"error": "Bad request"}, 400

    username = body.get("username", None)
    password = body.get("password", None)

    if not username or not password:
        return {"error": "Username and password is required"}, 400

    data = await current_app.db.fetch_one(
        "SELECT * FROM users WHERE username=:username", {"username": username}
    )

    if not data:
        return {"error": "Invalid username or password"}, 401

    valid = check_password_hash(data["password"], password)

    if not valid:
        return {"error": "Invalid username or password"}, 401

    user = dict(data)
    user.pop("password")
    token = get_token(user)

    return token


async def register():
    try:
        body = json.loads(await request.data)
    except json.JSONDecodeError:
        return {"error": "Bad request"}, 400

    username = body.get("username", None)
    password = body.get("password", None)
    email = body.get("email", None)

    if not username or not password:
        return {"error": "Username and password is required"}, 400

    data = await current_app.db.fetch_one(
        "SELECT * FROM users WHERE username=:username", {"username": username}
    )

    if data:
        return {"error": "Username already exists"}, 409

    password_hash = generate_password_hash(password)

    await current_app.db.execute(
        """
        INSERT INTO users (username, email, password) 
        VALUES (:username, :email, :password)
        """,
        {"username": username, "password": password_hash, "email": email},
    )

    return {"success": "Registration succesfull"}, 201


async def refresh():
    try:
        body = json.loads(await request.data)
    except json.JSONDecodeError:
        return {"error": "Bad request"}, 400

    token = body.get("refreshToken", None)

    if not token:
        {"error": "Bad request"}, 400

    try:
        payload = jwt.decode(
            token,
            current_app.config["REFRESH_SECRET"],
            algorithms=[
                "HS256",
            ],
        )
    except InvalidSignatureError:
        return {"error": "Invalid token"}, 401
    except ExpiredSignatureError:
        return {"error": "Token expired"}, 400

    token = get_token(payload)

    return token


@protected
async def test():
    return "Hello"
