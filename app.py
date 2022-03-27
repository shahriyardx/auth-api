import asyncio

from basicauth import app
from basicauth.helpers.db import _get_database_connection, indexes, schemas


@app.cli.command()
def initdb():
    loop = asyncio.get_event_loop()
    con = loop.run_until_complete(_get_database_connection(app))

    for schema in schemas + indexes:
        loop.run_until_complete(con.execute(schema))

    print("Database initialized")
