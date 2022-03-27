from asyncpg import create_pool
from quart import Quart

from .apps.auth import auth
from .config import config
from .helpers.db import DbHandler, _get_database_connection
from .urls import url_patterns

app = Quart(__name__)
app.config.from_object(config["development"])

app.register_blueprint(auth)

for path in url_patterns:
    app.add_url_rule(rule=path.url, view_func=path.view_func, methods=path.methods)


@app.before_first_request
async def before():
    db_pool = await _get_database_connection(app)
    app.db = DbHandler(db_pool)
