from contextlib import contextmanager
from .utils.sessions import session_scope


class BaseManager(object):
    @contextmanager
    @staticmethod
    def transaction():
        with session_scope() as session:
            yield session
