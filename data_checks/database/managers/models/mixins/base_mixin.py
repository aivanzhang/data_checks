from sqlalchemy import DateTime
import datetime
from sqlalchemy.orm import mapped_column, Mapped

"""
This mixin is used to add common columns to all models.
"""


class BaseMixin:
    __tablename__: str
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )
