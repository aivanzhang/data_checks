from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from data_checks.database.managers.models.mixins import BaseMixin

"""
This is a mixin for the main models.
"""


class MainMixin(BaseMixin):
    name: Mapped[str] = mapped_column(String(255))
