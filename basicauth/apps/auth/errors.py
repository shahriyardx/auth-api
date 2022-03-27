from basicauth.helpers.excecptions import Unauthorized

from . import auth


@auth.app_errorhandler(404)
async def not_found(e):
    return {"error": "Route not found"}, 404


@auth.app_errorhandler(Unauthorized)
async def unauthorized(e):
    return {"error": "Unauthorized"}, 401
