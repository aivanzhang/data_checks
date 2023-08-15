from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.mixins import MainManagerMixin
from data_checks.database.managers.models import Rule, Suite, SuiteExecution
from data_checks.database.utils.session_utils import session_scope


class SuiteManager(BaseManager, MainManagerMixin):
    model = Suite

    @staticmethod
    def create_suite(
        name: str,
        code: str,
        description: Optional[str] = None,
        excluded_check_tags: list[str] = [],
        rules: list["Rule"] = [],
        executions: list["SuiteExecution"] = [],
    ) -> Suite:
        new_suite = Suite.create(
            name=name,
            description=description,
            code=code,
            rules=rules,
            excluded_check_tags=excluded_check_tags,
            executions=executions,
        )
        with session_scope() as session:
            session.add(new_suite)
        return new_suite
