import re

from asyncpg import Pool, create_pool

schemas = [
    """DROP TABLE IF EXISTS users;""",
    """
    CREATE TABLE IF NOT EXISTS users (
              id BIGSERIAL PRIMARY KEY NOT NULL,
        username VARCHAR(20) NOT NULL,
           email VARCHAR(255) NULL,
        password VARCHAR(1024) NOT NULL
    );
    """,
]

indexes = ["""CREATE INDEX idx_users_username_email ON users(username, email)"""]


async def _get_database_connection(app) -> Pool:
    return await create_pool(app.config["DATABASE"])


class DbHandler:
    def __init__(self, database: Pool):
        self.database = database

    def get_data(self, query, values=None):
        if not values:
            return [query, []]

        items = []
        vars = re.findall(r"(:[a-zA-Z_]+)", query)

        for index, match in enumerate(vars):
            var = match[1:]
            items.append(values[var])
            query = query.replace(match, f"${index+1}")

        return [query, items]

    async def fetch_one(self, query, values=None):
        nq, nv = self.get_data(query, values)

        async with self.database.acquire() as con:
            data = await con.fetchrow(nq, *nv)
            return data

    async def fetch_all(self, query, values=None):
        nq, nv = self.get_data(query, values)
        async with self.database.acquire() as con:
            data = await con.fetch(nq, *nv)
            return data

    async def fetch_val(self, query, values=None):
        nq, nv = self.get_data(query, values)
        async with self.database.acquire() as con:
            data = await con.fetchval(nq, *nv)
            return data

    async def execute(self, query, values=None):
        nq, nv = self.get_data(query, values)
        async with self.database.acquire() as con:
            await con.execute(nq, *nv)
