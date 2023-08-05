from typing import Optional
from .base_manager import BaseManager
from .models import Rule, Suite, SuiteExecution


class SuiteManager(BaseManager):
    @classmethod
    def create_suite(
        cls,
        name: str,
        code: str,
        readable_name: Optional[str] = None,
        description: Optional[str] = None,
        excluded_check_tags: list[str] = [],
        rules: list["Rule"] = [],
        executions: list["SuiteExecution"] = [],
    ) -> Suite:
        new_suite = Suite.create(
            name=name,
            readable_name=readable_name,
            description=description,
            code=code,
            rules=rules,
            excluded_check_tags=excluded_check_tags,
            executions=executions,
        )
        return new_suite
