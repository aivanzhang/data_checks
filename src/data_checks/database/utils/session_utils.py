from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, scoped_session

DataCheckSession = sessionmaker(expire_on_commit=False)


def configure(bind: Engine, **kwargs):
    global DataCheckSession
    DataCheckSession.configure(bind=bind, **kwargs)
    DataCheckSession = scoped_session(DataCheckSession)


def get_session():
    return DataCheckSession()
