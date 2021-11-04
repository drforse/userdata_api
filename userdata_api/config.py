import os
from pathlib import Path

from sqlalchemy.engine import url as sa_url
from dotenv import load_dotenv, dotenv_values

load_dotenv()
default_env = dotenv_values(".env.default")


def _getenv(key: str, type_: type = str):
    env = os.environ.get(key) or default_env[key]
    return type_(env)


HOST = _getenv("USERDATA_API_LISTEN_HOST")
PORT = _getenv("USERDATA_API_LISTEN_PORT", int)
PHOTOS_PUBLIC_URL_BASE = _getenv("PHOTOS_API_PUBLIC_URL_BASE")
PHOTOS_PATH_BASE = Path.cwd() / "photos"
CREDS_PATH = Path(_getenv("USERDATA_API_CREDS_DIR")) / "creds.bin"
DB_ADDRESS = _getenv("DB_ADDRESS")
SA_URL = sa_url.make_url(DB_ADDRESS)
DEBUG = bool(_getenv("DEBUG", int))
