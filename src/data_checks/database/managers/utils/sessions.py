from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

DataCheckSession = sessionmaker()


def configure(bind: Engine, **kwargs):
    global DataCheckSession
    DataCheckSession.configure(bind=bind, **kwargs)
    DataCheckSession = scoped_session(DataCheckSession)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = DataCheckSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
