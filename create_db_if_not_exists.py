from os import getenv

from dotenv import load_dotenv, dotenv_values
from loguru import logger
from sqlalchemy.engine import url as sa_url
from sqlalchemy_utils import database_exists, create_database


if __name__ == "__main__":
    load_dotenv()
    default_env = dotenv_values(".env.default")
    DB_ADDRESS = getenv("DB_ADDRESS") or default_env["DB_ADDRESS"]
    SA_URL = sa_url.make_url(DB_ADDRESS)

    if not database_exists(SA_URL):
        create_database(SA_URL)
        logger.info("database created")
    else:
        logger.info("database already exists")
