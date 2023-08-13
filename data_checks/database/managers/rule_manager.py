from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, RuleExecution
from data_checks.database.utils.session_utils import session_scope


class RuleManager(BaseManager):
    @staticmethod
    def create_rule(
        name: str,
        code: str,
        readable_name: Optional[str] = None,
        description: Optional[str] = None,
        severity: float = 0.0,
        schedule: Optional[str] = None,
        tags: list[str] = [],
        executions: list["RuleExecution"] = [],
    ) -> Rule:
        new_rule = Rule.create(
            name=name,
            code=code,
            readable_name=readable_name,
            description=description,
            severity=severity,
            schedule=schedule,
            tags=tags,
            executions=executions,
        )
        with session_scope() as session:
            session.add(new_rule)
        return new_rule

    @staticmethod
    def update_suite_id(rule_id: int, suite_id: int):
        with session_scope() as session:
            session.query(Rule).filter_by(id=rule_id).update(
                {
                    "suite_id": suite_id,
                }
            )

    @staticmethod
    def update_check_id(rule_id: int, check_id: int):
        with session_scope() as session:
            session.query(Rule).filter_by(id=rule_id).update(
                {
                    "check_id": check_id,
                }
            )
