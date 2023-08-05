from .utils.sessions import session_scope


class BaseManager(object):
    @staticmethod
    def save():
        with session_scope() as session:
            session.commit()
