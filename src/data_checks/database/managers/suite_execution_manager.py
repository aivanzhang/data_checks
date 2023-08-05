from typing import Optional
from datetime import datetime
from .base_manager import BaseManager
from .models import Suite, SuiteExecution
from .utils.sessions import session_scope


class SuiteExecutionManager(BaseManager):
    @staticmethod
    def create_suite_execution(
        suite: Suite,
        status: Optional[str] = None,
        params: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ) -> SuiteExecution:
        new_execution = SuiteExecution.create(
            suite=suite,
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
            session.query(SuiteExecution).filter_by(id=execution_id).update(
                {
                    "status": status,
                    "params": params,
                    "logs": logs,
                    "traceback": traceback,
                    "exception": exception,
                    "finished_at": finished_at,
                }
            )
