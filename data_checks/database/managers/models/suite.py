from typing import List
from sqlalchemy import String, UnicodeText, ARRAY
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, Rule, SuiteExecution
from data_checks.database.managers.models.mixins import MainMixin


class Suite(Base, MainMixin):
    __tablename__ = "suites"
    excluded_check_tags: Mapped[List[str]] = mapped_column(
        ARRAY(String(255)), default=[]
    )
    code: Mapped[str] = mapped_column(UnicodeText())

    rules: Mapped[List["Rule"]] = relationship(back_populates="suite")
    executions: Mapped[List["SuiteExecution"]] = relationship(
        back_populates="main_model"
    )

    def __repr__(self) -> str:
        return (
            f"Suite(id={self.id!r}, name={self.name!r}, executions={self.executions!r})"
        )
