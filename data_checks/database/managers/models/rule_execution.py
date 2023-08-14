from sqlalchemy import UnicodeText
from sqlalchemy.orm import mapped_column, Mapped
from data_checks.database.managers.models.classes import Base
from data_checks.database.managers.models.mixins import ExecutionMixin


class RuleExecution(Base, ExecutionMixin):
    __tablename__ = "rule_executions"

    params = mapped_column(UnicodeText(), nullable=True)
    logs: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    traceback: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    exception = mapped_column(UnicodeText(), nullable=True)

    def __repr__(self) -> str:
        return f"RuleExecution(id={self.id!r}, check={self.main_model!r})"
