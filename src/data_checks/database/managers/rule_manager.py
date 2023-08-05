from typing import Optional
from .base_manager import BaseManager
from .models import Rule, RuleExecution


class RuleManager(BaseManager):
    @classmethod
    def create_rule(
        cls,
        name: str,
        code: str,
        readable_name: Optional[str] = None,
        description: Optional[str] = None,
        severity: float = 0.0,
        tags: list[str] = [],
        executions: list["RuleExecution"] = [],
    ) -> Rule:
        new_rule = Rule.create(
            name=name,
            readable_name=readable_name,
            description=description,
            code=code,
            tags=tags,
            severity=severity,
            executions=executions,
        )
        return new_rule
