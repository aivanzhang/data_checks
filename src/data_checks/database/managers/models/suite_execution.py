import datetime
from sqlalchemy import ForeignKey, func, DateTime, String, UnicodeText
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .classes import Base, Suite


class SuiteExecution(Base):
    __tablename__ = "suite_executions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    suite_id: Mapped[int] = mapped_column(ForeignKey("suites.id"))
    suite: Mapped["Suite"] = relationship(back_populates="executions")
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
        return f"SuiteExecution(id={self.id!r}, check={self.suite!r})"
