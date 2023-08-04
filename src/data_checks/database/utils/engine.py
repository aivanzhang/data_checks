from typing import Optional
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base

engine: Optional[Engine] = None

Session: Optional[sessionmaker] = None


def is_engine_defined():
    return engine is not None


def _init_database():
    global engine
    if engine is not None:
        Base.metadata.create_all(engine)
        global Session
        Session = sessionmaker(bind=engine)


def start(db_engine: Engine):
    global engine
    engine = db_engine
    _init_database()


def connect(url: str, **kwargs):
    global engine
    engine = create_engine(url, **kwargs)
    _init_database()


def get_engine() -> Engine:
    if engine is None:
        raise Exception("Engine is not defined")
    return engine


def get_session() -> sessionmaker:
    if Session is None:
        raise Exception("Session is not defined")
    return Session()
