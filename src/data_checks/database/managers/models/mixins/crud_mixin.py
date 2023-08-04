from sqlalchemy.orm import Session
from src.data_checks.database.utils import get_session


class CRUDMixin(object):
    session: Session

    @classmethod
    def set_session(cls, session):
        cls.session = session

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls.session.add(instance)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self

    def save(self):
        self.session.add(self)
        self.session.commit()
        return self
