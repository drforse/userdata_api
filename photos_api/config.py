import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path.cwd() / "config.ini", encoding="utf-8")

HOST = config.get("photos_api", "host")
PORT = config.getint("photos_api", "port")
CREDS_PATH = Path(config.get("photos_api", "creds_directory")) / "creds.bin"
