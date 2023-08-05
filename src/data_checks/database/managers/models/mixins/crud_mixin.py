from ...utils.sessions import session_scope


class CRUDMixin(object):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.add()
        return instance

    def add(self):
        with session_scope() as session:
            session.add(self)

    def update(self, **kwargs):
        with session_scope() as session:
            return self

    def save(self):
        with session_scope() as session:
            session.add(self)
            session.commit()
        return self
