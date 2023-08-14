from data_checks.database.managers.models.classes import Base
from data_checks.database.managers.models.mixins import ExecutionMixin


class CheckExecution(Base, ExecutionMixin):
    __tablename__ = "check_executions"

    def __repr__(self) -> str:
        return f"CheckExecution(id={self.id!r})"
