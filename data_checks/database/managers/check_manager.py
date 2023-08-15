from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Check, CheckExecution, Rule
from data_checks.database.managers.mixins import MainManagerMixin
from data_checks.database.utils.session_utils import session_scope


class CheckManager(BaseManager, MainManagerMixin):
    model = Check

    @staticmethod
    def create_check(
        name: str,
        code: str,
        description: Optional[str] = None,
        tags: list[str] = [],
        excluded_rules: list[str] = [],
        rules: list["Rule"] = [],
        executions: list["CheckExecution"] = [],
    ) -> Check:
        new_check = Check.create(
            name=name,
            description=description,
            code=code,
            tags=tags,
            excluded_rules=excluded_rules,
            rules=rules,
            executions=executions,
        )
        with session_scope() as session:
            session.add(new_check)
        return new_check

    @staticmethod
    def latest_version(name: str) -> Check:
        with session_scope() as session:
            return (
                session.query(Check)
                .filter_by(name=name)
                .order_by(Check.created_at.desc())
                .limit(1)
                .one()
            )
