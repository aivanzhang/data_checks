from sqlalchemy import func
from data_checks.database.managers.models.mixins import ExecutionMixin
from data_checks.database.utils.session_utils import session_scope


class ExecutionManagerMixin:
    model: type[ExecutionMixin]

    @classmethod
    def latest(cls) -> list[ExecutionMixin]:
        with session_scope() as session:
            subquery = (
                session.query(
                    cls.model.main_id,
                    func.max(cls.model.created_at).label("max_created_at"),
                )
                .group_by(cls.model.main_id)
                .subquery()
            )

            latest_items = (
                session.query(cls.model)
                .join(
                    subquery,
                    (cls.model.main_id == subquery.c.name)
                    & (cls.model.created_at == subquery.c.max_created_at),
                )
                .all()
            )

        print(latest_items)

        return latest_items
