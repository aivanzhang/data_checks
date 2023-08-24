from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Check, Rule
from data_checks.database.utils.session_utils import session_scope


class CheckManager(BaseManager):
    model = Check

    @staticmethod
    def create_check(
        name: str,
        code: str,
        excluded_rules: list[str] = [],
        config: Optional[str] = None,
        rules: list["Rule"] = [],
    ) -> Check:
        new_check = Check.create(
            name=name,
            code=code,
            excluded_rules=excluded_rules,
            config=config,
            rules=rules,
        )
        with session_scope() as session:
            session.add(new_check)
        return new_check

    @staticmethod
    def latest(name: str) -> Optional[Check]:
        with session_scope() as session:
            return (
                session.query(Check)
                .filter(Check.name == name)
                .order_by(Check.created_at.desc())
                .first()
            )
