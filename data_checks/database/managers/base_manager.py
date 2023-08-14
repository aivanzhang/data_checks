from contextlib import contextmanager
from data_checks.database.utils.session_utils import session_scope
from data_checks.database.managers.models.classes import Base


class BaseManager(object):
    model: type[Base]

    @contextmanager
    @staticmethod
    def transaction():
        with session_scope() as session:
            yield session

    # @classmethod
    # def get_latest(cls) -> list[Base]:
    #     with session_scope() as session:
    #         subquery = (
    #             session.query(
    #                 cls.model.name,
    #                 func.max(cls.model.created_at).label("max_created_at"),
    #             )
    #             .group_by(cls.model.name)
    #             .subquery()
    #         )

    #         latest_items = (
    #             session.query(cls.model)
    #             .join(
    #                 subquery,
    #                 (cls.model.name == subquery.c.name)
    #                 & (cls.model.created_at == subquery.c.max_created_at),
    #             )
    #             .all()
    #         )
    #         items = session.query(cls.model).all()
    #     return items
