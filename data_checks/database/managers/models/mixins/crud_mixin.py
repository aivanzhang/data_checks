from data_checks.database.utils.session_utils import session_scope


class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def save(self):
        with session_scope() as session:
            session.add(self)
