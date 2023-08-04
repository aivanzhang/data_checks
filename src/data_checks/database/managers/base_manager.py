from sqlalchemy.orm import Session


class BaseManager(object):
    session: Session

    @classmethod
    def set_session(cls, session):
        cls.session = session

    @classmethod
    def save(cls):
        cls.session.commit()
