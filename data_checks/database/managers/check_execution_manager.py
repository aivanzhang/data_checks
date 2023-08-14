from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.mixins.execution_manager_mixins import (
    ExecutionManagerMixin,
)
from data_checks.database.managers.models import CheckExecution


class CheckExecutionManager(BaseManager, ExecutionManagerMixin[CheckExecution]):
    model: type[CheckExecution] = CheckExecution
