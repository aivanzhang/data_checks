from typing import List
import datetime
from sqlalchemy import String, UnicodeText, ARRAY, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import (
    Base,
    RuleExecution,
    Check,
    Suite,
)


class Rule(Base):
    __tablename__ = "rules"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    readable_name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    severity: Mapped[float] = mapped_column(Numeric(6, 3), default=0.0)
    tags: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])
    code: Mapped[str] = mapped_column(UnicodeText())
    schedule: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )

    suite_id: Mapped[int] = mapped_column(ForeignKey("suites.id"), nullable=True)
    suite: Mapped["Suite"] = relationship(back_populates="rules")
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"), nullable=True)
    check: Mapped["Check"] = relationship(back_populates="rules")
    executions: Mapped[List["RuleExecution"]] = relationship(back_populates="rule")

    def __repr__(self) -> str:
        return (
            f"Rule(id={self.id!r}, name={self.name!r}, executions={self.executions!r})"
        )
