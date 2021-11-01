import hashlib

from . import config


def is_correct_api_key(key: str) -> bool:
    with open(config.CREDS_PATH, "rb") as f:
        correct_hash, salt = f.read().split(b'\n\n')
    input_hash = hashlib.scrypt(
        key.encode("utf-8"),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )
    return input_hash == correct_hash
