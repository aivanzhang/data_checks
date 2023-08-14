from data_checks.database.managers.models.classes import Base
from data_checks.database.managers.models.mixins import ExecutionMixin


class SuiteExecution(Base, ExecutionMixin):
    __tablename__ = "suite_executions"

    def __repr__(self) -> str:
        return f"SuiteExecution(id={self.id!r})"
