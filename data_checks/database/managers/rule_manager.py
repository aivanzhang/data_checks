from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, RuleExecution
from data_checks.database.utils.session_utils import session_scope


class RuleManager(BaseManager):
    model = Rule

    @staticmethod
    def generate_hash(
        name: str,
        check_name: Optional[str],
        group: Optional[str],
        suite_name: Optional[str],
        params: str,
    ) -> str:
        hash_value = f"rule:{name}::params:{params}"
        if group:
            hash_value = f"group:{group}::{hash_value}"
        if check_name:
            hash_value = f"check:{check_name}::{hash_value}"
        if suite_name:
            hash_value = f"suite:{suite_name}::{hash_value}"
        return hash_value

    @staticmethod
    def create_rule(
        name: str,
        code: str,
        params: str,
        check_id: Optional[int] = None,
        check_name: Optional[str] = None,
        group: Optional[str] = None,
        suite_id: Optional[int] = None,
        suite_name: Optional[str] = None,
        severity: float = 0.0,
        executions: list["RuleExecution"] = [],
    ) -> Rule:
        new_rule = Rule.create(
            name=name,
            check_id=check_id,
            suite_id=suite_id,
            hash=RuleManager.generate_hash(
                name=name,
                check_name=check_name,
                group=group,
                suite_name=suite_name,
                params=params,
            ),
            group=group,
            code=code,
            severity=severity,
            executions=executions,
        )
        with session_scope() as session:
            session.add(new_rule)
        return new_rule

    @staticmethod
    def latest(
        suite_name: Optional[str],
        check_name: Optional[str],
        name: str,
        params: str,
        group: Optional[str] = None,
    ) -> Optional[Rule]:
        with session_scope() as session:
            return (
                session.query(Rule)
                .filter_by(
                    hash=RuleManager.generate_hash(
                        name=name,
                        check_name=check_name,
                        group=group,
                        suite_name=suite_name,
                        params=params,
                    ),
                    group=group,
                )
                .order_by(Rule.created_at.desc())
                .first()
            )
