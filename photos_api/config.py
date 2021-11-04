import os
from pathlib import Path

from dotenv import load_dotenv, dotenv_values

load_dotenv()
default_env = dotenv_values(".env.default")


def _getenv(key: str, type_: type = str):
    env = os.environ.get(key) or default_env[key]
    return type_(env)


HOST = _getenv("PHOTOS_API_LISTEN_HOST")
PORT = _getenv("PHOTOS_API_LISTEN_PORT", int)
CREDS_PATH = Path(_getenv("PHOTOS_API_CREDS_DIR")) / "creds.bin"
DEBUG = bool(_getenv("DEBUG", int))
