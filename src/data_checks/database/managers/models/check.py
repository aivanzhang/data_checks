from typing import List
import datetime
from sqlalchemy import String, UnicodeText, ARRAY, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .classes import Base, CheckExecution, Rule


class Check(Base):
    __tablename__ = "checks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    readable_name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    code: Mapped[str] = mapped_column(UnicodeText())
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    tags: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])
    excluded_rules: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])

    rules: Mapped[List["Rule"]] = relationship(back_populates="check")
    executions: Mapped[List["CheckExecution"]] = relationship(back_populates="check")

    def __repr__(self) -> str:
        return (
            f"Check(id={self.id!r}, name={self.name!r}, executions={self.executions!r})"
        )
