from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, RuleExecution
from data_checks.database.utils.session_utils import session_scope


class RuleManager(BaseManager):
    model = Rule

    @staticmethod
    def generate_hash(
        name: str, check_name: Optional[str], suite_name: Optional[str], params: str
    ) -> str:
        check_name = check_name or "NONENONE"
        suite_name = suite_name or "NONENONE"
        return f"{name}_{check_name}_{suite_name}_{params}"

    @staticmethod
    def create_rule(
        name: str,
        code: str,
        params: str,
        check_id: Optional[int] = None,
        check_name: Optional[str] = None,
        suite_id: Optional[int] = None,
        suite_name: Optional[str] = None,
        severity: float = 0.0,
        executions: list["RuleExecution"] = [],
    ) -> Rule:
        new_rule = Rule.create(
            name=name,
            check_id=check_id,
            suite_id=suite_id,
            hash=RuleManager.generate_hash(name, check_name, suite_name, params),
            code=code,
            severity=severity,
            executions=executions,
        )
        with session_scope() as session:
            session.add(new_rule)
        return new_rule

    @staticmethod
    def latest(
        suite_name: Optional[str], check_name: Optional[str], name: str, params: str
    ) -> Optional[Rule]:
        with session_scope() as session:
            return (
                session.query(Rule)
                .filter_by(
                    hash=RuleManager.generate_hash(name, check_name, suite_name, params)
                )
                .order_by(Rule.created_at.desc())
                .first()
            )
