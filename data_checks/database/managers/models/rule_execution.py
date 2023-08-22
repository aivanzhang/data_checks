import datetime
from sqlalchemy import UnicodeText
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, ForeignKey
from data_checks.database.managers.models.classes import Base
from data_checks.database.managers.models.mixins import BaseMixin


class RuleExecution(Base, BaseMixin):
    __tablename__ = "rule_executions"

    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"), nullable=False)
    rule = relationship("Rule", back_populates="executions")
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    params = mapped_column(UnicodeText(), nullable=True)
    logs: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    traceback: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    exception = mapped_column(UnicodeText(), nullable=True)

    def __repr__(self) -> str:
        return f"RuleExecution(id={self.id!r})"
