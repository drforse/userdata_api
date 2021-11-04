import sys
import multiprocessing

from loguru import logger
from sanic import Sanic
from sanic.request import Request
from sanic_restful_api import Api, abort, reqparse

from . import config
from .db import Base, engine
from .auth_utils import is_correct_api_key
from .resources import UsersResource, UserResource


def main():
    """registers middleware for authorization and runs the app"""
    app = Sanic(__name__)

    parser = reqparse.RequestParser()
    parser.add_argument("api_key", type=str, location="args")

    @app.middleware("request")
    async def auth_middleware(request: Request):
        api_key = parser.parse_args(request).api_key
        if api_key is None or is_correct_api_key(api_key) is False:
            abort(401)

    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if config.DEBUG else "INFO", enqueue=True)

    api = Api(app)
    api.add_resource(UsersResource, "/api/users", methods=["POST"])
    api.add_resource(UserResource, "/api/users/<user_id>", methods=["GET", "DELETE"])

    from . import models
    Base.metadata.create_all(engine)

    try:
        app.run(
            config.HOST, config.PORT,
            debug=config.DEBUG, auto_reload=False,
            workers=1 if config.DEBUG else multiprocessing.cpu_count()
        )
    except (KeyboardInterrupt, SystemExit) as e:
        logger.info("Good Bye!")
