from typing import Optional
from datetime import datetime
from .base_manager import BaseManager
from .models import Rule, RuleExecution
from .utils.session_utils import session_scope
from .utils.database_utils import generate_update_object


class RuleExecutionManager(BaseManager):
    @staticmethod
    def create_rule_execution(
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
        with session_scope() as session:
            session.add(new_execution)
        return new_execution

    @staticmethod
    def update_execution(
        execution_id: int,
        finished_at: datetime = datetime.now(),
        status: Optional[str] = None,
        params: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ):
        with session_scope() as session:
            session.query(RuleExecution).filter_by(id=execution_id).update(
                generate_update_object(
                    status=status,
                    params=params,
                    logs=logs,
                    traceback=traceback,
                    exception=exception,
                    finished_at=finished_at,
                )
            )
