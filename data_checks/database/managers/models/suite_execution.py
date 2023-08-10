import datetime
from sqlalchemy import ForeignKey, DateTime, String, UnicodeText
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, Suite


class SuiteExecution(Base):
    __tablename__ = "suite_executions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    suite_id: Mapped[int] = mapped_column(ForeignKey("suites.id"))
    suite: Mapped["Suite"] = relationship(back_populates="executions")
    status: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"SuiteExecution(id={self.id!r}, check={self.suite!r})"
