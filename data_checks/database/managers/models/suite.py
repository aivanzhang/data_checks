from typing import List
from sqlalchemy import String, UnicodeText
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.classes import Base, Rule
from data_checks.database.managers.models.mixins import MainMixin


class Suite(Base, MainMixin):
    __tablename__ = "suites"

    code: Mapped[str] = mapped_column(UnicodeText())
    rules: Mapped[List["Rule"]] = relationship(back_populates="suite")
    config: Mapped[str] = mapped_column(UnicodeText(), nullable=True)

    def __repr__(self) -> str:
        return f"Suite(id={self.id!r}, name={self.name!r})"
