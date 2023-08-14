from sqlalchemy import func
from data_checks.database.managers.models.mixins import MainMixin
from data_checks.database.utils.session_utils import session_scope


class MainManagerMixin:
    model: type[MainMixin]

    @classmethod
    def latest(cls) -> list[MainMixin]:
        with session_scope() as session:
            subquery = (
                session.query(
                    cls.model.name,
                    func.max(cls.model.created_at).label("max_created_at"),
                )
                .group_by(cls.model.name)
                .subquery()
            )

            latest_items = (
                session.query(cls.model)
                .join(
                    subquery,
                    (cls.model.name == subquery.c.name)
                    & (cls.model.created_at == subquery.c.max_created_at),
                )
                .all()
            )

        print(latest_items)

        return latest_items
