from typing import Optional
from datetime import datetime
from data_checks.database.managers.base_manager import BaseManager
from data_checks.database.managers.mixins.execution_manager_mixins import (
    ExecutionManagerMixin,
)
from data_checks.database.managers.models import SuiteExecution


class SuiteExecutionManager(BaseManager, ExecutionManagerMixin[SuiteExecution]):
    model: type[SuiteExecution] = SuiteExecution
