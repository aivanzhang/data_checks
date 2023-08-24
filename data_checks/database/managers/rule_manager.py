from typing import Optional
import datetime
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Rule, RuleExecution, Check, Suite
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
        params = params.replace('"', "")
        hash_value = f"rule:{name}::params:{params}"
        if group:
            group = group.replace('"', "")
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
        config: Optional[str] = None,
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
                )
                .order_by(Rule.created_at.desc())
                .first()
            )

    @staticmethod
    def silence_by_hash(until: datetime.datetime, hash: str) -> bool:
        with session_scope() as session:
            rule = session.query(Rule).filter_by(hash=hash).first()
            if rule:
                rule.silenced_until = until
                session.add(rule)
                return True

        return False

    @staticmethod
    def silence(
        until: datetime.datetime,
        name: str,
        check_name: Optional[str] = None,
        suite_name: Optional[str] = None,
    ) -> bool:
        with session_scope() as session:
            rules = (
                session.query(Rule)
                .join(Check)
                .join(Suite)
                .filter(Rule.name == name)
                .filter(Check.name == check_name)
                .filter(Suite.name == suite_name)
                .all()
            )
            if rules:
                for rule in rules:
                    rule.silenced_until = until
                    session.add(rule)
                return True

        return False
