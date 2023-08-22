from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, Suite
from data_checks.database.utils.session_utils import session_scope


class SuiteManager(BaseManager):
    model = Suite

    @staticmethod
    def create_suite(
        name: str,
        code: str,
        schedule: Optional[str] = None,
        description: Optional[str] = None,
        rules: list["Rule"] = [],
    ) -> Suite:
        new_suite = Suite.create(
            name=name,
            schedule=schedule,
            description=description,
            code=code,
            rules=rules,
        )
        with session_scope() as session:
            session.add(new_suite)
        return new_suite

    @staticmethod
    def latest(
        name: str,
    ) -> Optional[Suite]:
        with session_scope() as session:
            return (
                session.query(Suite)
                .filter(Suite.name == name)
                .order_by(Suite.created_at.desc())
                .first()
            )
