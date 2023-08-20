from typing import List
from sqlalchemy import String, UnicodeText, ARRAY
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, Rule
from data_checks.database.managers.models.mixins import MainMixin


class Check(Base, MainMixin):
    __tablename__ = "checks"

    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    code: Mapped[str] = mapped_column(UnicodeText())
    excluded_rules: Mapped[List[str]] = mapped_column(ARRAY(String(255)), default=[])
    rules: Mapped[List["Rule"]] = relationship(back_populates="check")

    def __repr__(self) -> str:
        return f"Check(id={self.id!r}, name={self.name!r})"
