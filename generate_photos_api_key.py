from os import getenv
from pathlib import Path
from uuid import uuid4
import hashlib

from dotenv import dotenv_values, load_dotenv

load_dotenv()
default_env = dotenv_values(".env.default")

creds_directory = Path(getenv("PHOTOS_API_CREDS_DIR") or default_env["PHOTOS_API_CREDS_DIR"])
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
