import datetime
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, Check


class CheckExecution(Base):
    __tablename__ = "check_executions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"))
    check: Mapped["Check"] = relationship(back_populates="executions")
    status: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"CheckExecution(id={self.id!r}, check={self.check!r})"
