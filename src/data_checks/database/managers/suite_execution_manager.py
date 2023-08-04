from typing import Optional
from .base_manager import BaseManager
from .models import Suite, SuiteExecution


class SuiteExecutionManager(BaseManager):
    @classmethod
    def create_suite_exceution(
        cls,
        suite: Suite,
        status: Optional[str] = None,
        data: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ) -> SuiteExecution:
        new_execution = SuiteExecution(
            suite=suite,
            status=status,
            data=data,
            logs=logs,
            traceback=traceback,
            exception=exception,
        )

        cls.session.add(new_execution)
        return new_execution
