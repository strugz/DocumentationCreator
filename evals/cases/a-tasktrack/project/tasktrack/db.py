from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config

_engine = create_engine(Config.DATABASE_URL)
_Session = sessionmaker(bind=_engine)


def get_session():
    return _Session()
