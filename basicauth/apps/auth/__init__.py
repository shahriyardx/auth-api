from quart import Blueprint

from .urls import url_patterns

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

for path in url_patterns:
    auth.add_url_rule(rule=path.url, view_func=path.view_func, methods=path.methods)

from .errors import *
