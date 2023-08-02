from typing import Optional
from sqlalchemy import create_engine, Engine

engine: Optional[Engine] = None


def is_engine_defined():
    return engine is not None


def set_engine(engine_: Engine):
    global engine
    engine = engine_


def get_engine() -> Optional[Engine]:
    return engine


def init_database(url: str, **kwargs):
    global engine
    engine = create_engine(url, **kwargs)
