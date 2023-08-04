import datetime
from sqlalchemy import ForeignKey, func, DateTime, String, UnicodeText
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .classes import Base, Rule


class RuleExecution(Base):
    __tablename__ = "rule_executions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"))
    rule: Mapped["Rule"] = relationship(back_populates="executions")
    status: Mapped[str] = mapped_column(String(255), nullable=True)

    data = mapped_column(UnicodeText(), nullable=True)
    logs: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    traceback: Mapped[str] = mapped_column(UnicodeText(), nullable=True)
    exception = mapped_column(UnicodeText(), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"RuleExecution(id={self.id!r}, check={self.rule!r})"
