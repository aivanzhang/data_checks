from typing import Optional
from sqlalchemy import Engine
from .models import Base

engine: Optional[Engine] = None


def is_engine_defined():
    return engine is not None


def start(engine_: Engine):
    global engine
    engine = engine_
    Base.metadata.create_all(engine)


def get_engine() -> Optional[Engine]:
    return engine
