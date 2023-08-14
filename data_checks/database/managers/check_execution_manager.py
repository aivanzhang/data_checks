from datetime import datetime
from typing import Optional
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.mixins import ExecutionManagerMixin
from data_checks.database.managers.models import Check, CheckExecution
from data_checks.database.utils.session_utils import session_scope
from data_checks.database.utils.database_utils import generate_update_object


class CheckExecutionManager(BaseManager, ExecutionManagerMixin):
    model = CheckExecution

    @staticmethod
    def create_execution(
        main_model: Check,
        status: Optional[str] = None,
    ) -> CheckExecution:
        new_execution = CheckExecution.create(
            main_model=main_model,
            status=status,
        )
        with session_scope() as session:
            session.add(new_execution)

        return new_execution

    @staticmethod
    def update_execution(
        execution_id: int,
        finished_at: datetime = datetime.now(),
        status: Optional[str] = None,
    ):
        with session_scope() as session:
            session.query(CheckExecution).filter_by(id=execution_id).update(
                generate_update_object(
                    status=status,
                    finished_at=finished_at,
                )
            )
