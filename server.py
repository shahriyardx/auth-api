import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from basicauth import app

config = Config()
config.bind = [
    "localhost:8000",
]

try:
    import uvloop

    uvloop.install()
    print("[+] Using unloop")
except:
    pass

asyncio.run(serve(app, config))
