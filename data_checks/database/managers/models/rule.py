from typing import List
import datetime
from sqlalchemy import UnicodeText, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import (
    Base,
    RuleExecution,
    Check,
    Suite,
)
from data_checks.database.managers.models.mixins import MainMixin


class Rule(Base, MainMixin):
    __tablename__ = "rules"

    severity: Mapped[float] = mapped_column(Numeric(6, 3), default=0.0)
    code: Mapped[str] = mapped_column(UnicodeText())
    hash: Mapped[str] = mapped_column(UnicodeText(), nullable=False)
    config: Mapped[str] = mapped_column(UnicodeText(), nullable=True)

    suite_id: Mapped[int] = mapped_column(ForeignKey("suites.id"), nullable=True)
    suite: Mapped["Suite"] = relationship(back_populates="rules")
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"), nullable=True)
    check: Mapped["Check"] = relationship(back_populates="rules")
    executions: Mapped[List["RuleExecution"]] = relationship(back_populates="rule")

    def __repr__(self) -> str:
        return f"Rule(id={self.id!r}, name={self.name!r})"
