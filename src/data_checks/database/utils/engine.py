from typing import Optional
import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

engine: Optional[Engine]

DataCheckSession = sessionmaker()


def is_engine_defined():
    return engine is not None


def _init_database():
    global engine, DataCheckSession
    if engine is not None:
        DataCheckSession.configure(bind=engine)


def start():
    if engine is None:
        raise Exception("Engine is not defined")
    _init_database()


def connect(url: str, **kwargs) -> Engine:
    global engine
    engine = create_engine(url, **kwargs)
    _init_database()
    return engine


def get_engine() -> Engine:
    if engine is None:
        raise Exception("Engine is not defined")
    return engine


def get_session() -> Session:
    return DataCheckSession()
