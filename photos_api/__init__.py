import sys
from pathlib import Path
from urllib.request import Request

from loguru import logger
from sanic import Sanic
from sanic_restful_api import reqparse, abort

from .auth_utils import is_correct_api_key
from .config import HOST, PORT


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
    logger.add(sys.stderr, level="DEBUG", enqueue=True)

    app.static("/photos", Path.cwd() / "photos")

    try:
        app.run(HOST, PORT, debug=True, auto_reload=False)
    except (KeyboardInterrupt, SystemExit) as e:
        logger.info("Good Bye!")
