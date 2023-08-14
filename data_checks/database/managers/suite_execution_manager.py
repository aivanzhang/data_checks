from typing import Optional
from datetime import datetime
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.models import Suite, SuiteExecution
from data_checks.database.utils.session_utils import session_scope
from data_checks.database.utils.database_utils import generate_update_object


class SuiteExecutionManager(BaseManager):
    model = SuiteExecution

    @staticmethod
    def create_suite_execution(
        main_model: Suite,
        status: Optional[str] = None,
    ) -> SuiteExecution:
        new_execution = SuiteExecution.create(
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
            session.query(SuiteExecution).filter_by(id=execution_id).update(
                generate_update_object(
                    status=status,
                    finished_at=finished_at,
                )
            )
