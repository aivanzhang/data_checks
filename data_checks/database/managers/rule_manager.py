from typing import Optional
import datetime
import json
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, RuleExecution
from data_checks.database.utils.session_utils import session_scope


class RuleManager(BaseManager):
    model = Rule

    @staticmethod
    def generate_hash(
        name: str,
        check_name: Optional[str],
        suite_name: Optional[str],
        params: str,
    ) -> str:
        hash_value = f"rule:{name}::params:{params}"
        if check_name:
            hash_value = f"check:{check_name}::{hash_value}"
        if suite_name:
            hash_value = f"suite:{suite_name}::{hash_value}"
        return hash_value.replace('"', "")

    @staticmethod
    def create_rule(
        name: str,
        code: str,
        params: str,
        config: Optional[str] = None,
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
            hash=RuleManager.generate_hash(
                name=name,
                check_name=check_name,
                suite_name=suite_name,
                params=params,
            ),
            config=config,
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
    ) -> Optional[Rule]:
        with session_scope() as session:
            return (
                session.query(Rule)
                .filter_by(
                    hash=RuleManager.generate_hash(
                        name=name,
                        check_name=check_name,
                        suite_name=suite_name,
                        params=params,
                    ),
                )
                .order_by(Rule.created_at.desc())
                .first()
            )

    @staticmethod
    def silence(until: datetime.datetime, hash: str) -> bool:
        with session_scope() as session:
            rule = (
                session.query(Rule)
                .filter_by(hash=hash)
                .order_by(Rule.created_at.desc())
                .first()
            )
            if rule:
                rule_config = json.loads(rule.config)
                rule_config["silenced_until"] = until
                rule.config = json.dumps(rule_config, default=str)
                session.add(rule)
                return True

        return False
