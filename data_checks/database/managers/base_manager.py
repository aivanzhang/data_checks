from contextlib import contextmanager
from data_checks.database.utils.session_utils import session_scope


class BaseManager(object):
    @contextmanager
    @staticmethod
    def transaction():
        with session_scope() as session:
            yield session
