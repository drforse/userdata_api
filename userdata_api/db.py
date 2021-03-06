from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionTypeHint
from sqlalchemy_utils import create_database, database_exists

from . import config

if not database_exists(config.SA_URL):
    create_database(config.SA_URL)

engine = create_engine(config.SA_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def session_scope(s: SessionTypeHint = None) -> ContextManager[SessionTypeHint]:
    session = s or Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        if not s:
            session.close()


def session_decorator(func):
    async def wrapper(*args, **kwargs):
        with session_scope() as s:
            return await func(*args, session=s, **kwargs)
    return wrapper


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
