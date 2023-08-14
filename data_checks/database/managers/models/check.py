from typing import List
from sqlalchemy import String, UnicodeText, ARRAY
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, CheckExecution, Rule
from data_checks.database.managers.models.mixins import MainMixin


class Check(Base, MainMixin):
    __tablename__ = "checks"

    code: Mapped[str] = mapped_column(UnicodeText())
    tags: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])
    excluded_rules: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])

    rules: Mapped[List["Rule"]] = relationship(back_populates="check")
    executions: Mapped[List["CheckExecution"]] = relationship(
        back_populates="main_model"
    )

    def __repr__(self) -> str:
        return f"Check(id={self.id!r}, name={self.name!r})"
