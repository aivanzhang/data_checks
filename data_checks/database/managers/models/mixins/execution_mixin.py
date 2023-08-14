import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, mapped_column, Mapped
from data_checks.database.managers.models.mixins import BaseMixin

"""
This is a mixin for the execution models.
"""


class ExecutionMixin(BaseMixin):
    @declared_attr
    def main_id(cls):
        return mapped_column(
            ForeignKey(f"{cls.__tablename__.replace('_executions', '').lower()}s.id")
        )

    @declared_attr
    def main_model(cls):
        return relationship(
            cls.__tablename__.replace("_executions", "").capitalize(),
            back_populates="executions",
        )

    status: Mapped[str] = mapped_column(String(255), nullable=True)
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
