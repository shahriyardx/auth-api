from ...helpers.models import Path
from .views import authorize, refresh, register, test

url_patterns = [
    Path("/authorize", authorize, ["POST"]),
    Path("/register", register, ["POST"]),
    Path("/refresh", refresh, ["POST"]),
    Path("/test", test, ["GET"]),
]
