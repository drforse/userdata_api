import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path.cwd() / "config.ini", encoding="utf-8")

HOST = config.get("userdata_api", "host")
PORT = config.getint("userdata_api", "port")
PHOTOS_PUBLIC_URL_BASE = config.get("photos_api", "public_url_base")
PHOTOS_PATH_BASE = Path.cwd() / "photos"
CREDS_PATH = Path(config.get("userdata_api", "creds_directory")) / "creds.bin"
DB_ADDRESS = config.get("default", "db_address")
