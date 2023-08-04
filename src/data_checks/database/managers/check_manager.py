from typing import Optional
from .base_manager import BaseManager
from .models import Check, CheckExecution, Rule


class CheckManager(BaseManager):
    @classmethod
    def create_check(
        cls,
        name: str,
        code: str,
        readable_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: list[str] = [],
        excluded_rules: list[str] = [],
        rules: list["Rule"] = [],
        executions: list["CheckExecution"] = [],
    ) -> Check:
        new_check = Check(
            name=name,
            readable_name=readable_name,
            description=description,
            code=code,
            tags=tags,
            excluded_rules=excluded_rules,
            rules=rules,
            executions=executions,
        )

        cls.session.add(new_check)
        return new_check
