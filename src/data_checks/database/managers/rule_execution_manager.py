from typing import Optional
from .base_manager import BaseManager
from .models import Rule, RuleExecution


class RuleExecutionManager(BaseManager):
    @classmethod
    def create_rule_exceution(
        cls,
        rule: Rule,
        status: Optional[str] = None,
        params: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ) -> RuleExecution:
        new_execution = RuleExecution.create(
            rule=rule,
            status=status,
            params=params,
            logs=logs,
            traceback=traceback,
            exception=exception,
        )
        return new_execution
