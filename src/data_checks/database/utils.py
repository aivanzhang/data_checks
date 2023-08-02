from sqlalchemy import create_engine, Engine

engine: Engine


def set_engine(engine_: Engine):
    global engine
    engine = engine_


def get_engine() -> Engine:
    return engine


def init_database(url: str, **kwargs):
    global engine
    engine = create_engine(url, **kwargs)
