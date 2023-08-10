from typing import List
import datetime
from sqlalchemy import String, UnicodeText, ARRAY, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .classes import Base, Rule, SuiteExecution


class Suite(Base):
    __tablename__ = "suites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    readable_name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    excluded_check_tags: Mapped[List[str]] = mapped_column(
        ARRAY(String(255)), default=[]
    )
    code: Mapped[str] = mapped_column(UnicodeText())
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )

    rules: Mapped[List["Rule"]] = relationship(back_populates="suite")
    executions: Mapped[List["SuiteExecution"]] = relationship(back_populates="suite")

    def __repr__(self) -> str:
        return (
            f"Suite(id={self.id!r}, name={self.name!r}, executions={self.executions!r})"
        )
