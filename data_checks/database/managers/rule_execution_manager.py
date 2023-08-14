from typing import Optional
from datetime import datetime
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.mixins.execution_manager_mixins import (
    ExecutionManagerMixin,
)
from data_checks.database.managers.models import Rule, RuleExecution
from data_checks.database.utils.session_utils import session_scope
from data_checks.database.utils.database_utils import generate_update_object


class RuleExecutionManager(BaseManager, ExecutionManagerMixin):
    model: type[RuleExecution] = RuleExecution

    @classmethod
    def create_execution(
        cls,
        main_model: Rule,
        status: Optional[str] = None,
        params: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ) -> RuleExecution:
        new_execution = RuleExecution.create(
            main_model=main_model,
            status=status,
            params=params,
            logs=logs,
            traceback=traceback,
            exception=exception,
        )
        with session_scope() as session:
            session.add(new_execution)
        return new_execution

    @classmethod
    def update_execution(
        cls,
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
