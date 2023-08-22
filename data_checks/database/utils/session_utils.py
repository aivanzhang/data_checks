from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DataCheckSession = sessionmaker(expire_on_commit=False)


def configure(bind: Engine, **kwargs):
    global DataCheckSession
    DataCheckSession.configure(bind=bind, **kwargs)


def get_session():
    return DataCheckSession()


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
