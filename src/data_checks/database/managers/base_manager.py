from src.data_checks.database.utils import get_session


class BaseManager(object):
    def __init__(self):
        self.session = get_session()
