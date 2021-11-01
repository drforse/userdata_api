from pathlib import Path
from uuid import uuid4
import hashlib
import configparser

config = configparser.ConfigParser()
config.read(Path.cwd() / "config.ini", encoding="utf-8")


creds_directory = Path(config.get("photos_api", "creds_directory"))
if creds_directory.exists() is False:
    creds_directory.mkdir()


salt = str(uuid4()).encode("utf-8")
key_str = str(uuid4())

key = hashlib.scrypt(
    key_str.encode("utf-8"),
    salt=salt,
    n=16384,
    r=8,
    p=1
)

with open(creds_directory / "creds.bin", "wb") as f:
    f.write(key + b"\n\n" + salt)

print("photos api key: ", key_str)
