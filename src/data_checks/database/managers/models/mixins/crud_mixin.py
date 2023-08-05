from ...utils.sessions import session_scope


class CRUDMixin(object):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance

    def update(self, **kwargs):
        with session_scope() as session:
            for attr, value in kwargs.items():
                setattr(self, attr, value)
            session.add(self)
