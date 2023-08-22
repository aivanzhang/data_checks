from typing import Optional
from sqlalchemy import Engine, create_engine

engine: Optional[Engine]


def connect(url: str, **kwargs) -> Engine:
    global engine
    engine = create_engine(url, **kwargs)
    return engine


def get_engine():
    return engine
