from typing import Optional
from .base_manager import BaseManager
from .models import Check, CheckExecution


class CheckExecutionManager(BaseManager):
    @classmethod
    def create_check_exceution(
        cls,
        check: Check,
        status: Optional[str] = None,
        data: Optional[str] = None,
        logs: Optional[str] = None,
        traceback: Optional[str] = None,
        exception: Optional[str] = None,
    ) -> CheckExecution:
        new_execution = CheckExecution(
            check=check,
            status=status,
            data=data,
            logs=logs,
            traceback=traceback,
            exception=exception,
        )

        cls.session.add(new_execution)
        return new_execution
