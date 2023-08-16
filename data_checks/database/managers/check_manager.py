from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Check, Rule
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
    ) -> Check:
        new_check = Check.create(
            name=name,
            description=description,
            code=code,
            tags=tags,
            excluded_rules=excluded_rules,
            rules=rules,
        )
        with session_scope() as session:
            session.add(new_check)
        return new_check
