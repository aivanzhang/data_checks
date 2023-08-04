from typing import List
from sqlalchemy import String, UnicodeText, ARRAY, ForeignKey, Numeric
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .classes import Base, RuleExecution, Check, Suite


class Rule(Base):
    __tablename__ = "rules"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    readable_name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    severity: Mapped[float] = mapped_column(Numeric(6, 3), default=0.0)
    tags: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])
    code: Mapped[str] = mapped_column(UnicodeText())

    suite_id: Mapped[int] = mapped_column(ForeignKey("suites.id"))
    suite: Mapped["Suite"] = relationship(back_populates="rules")
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"))
    check: Mapped["Check"] = relationship(back_populates="rules")
    executions: Mapped[List["RuleExecution"]] = relationship(back_populates="rule")

    def __repr__(self) -> str:
        return (
            f"Rule(id={self.id!r}, name={self.name!r}, executions={self.executions!r})"
        )
