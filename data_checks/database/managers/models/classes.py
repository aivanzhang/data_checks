from sqlalchemy.orm import DeclarativeBase
from data_checks.database.managers.models.mixins import CRUDMixin


class Base(DeclarativeBase, CRUDMixin):
    pass


class Rule:
    pass


class RuleExecution:
    pass


class Check:
    pass


class Suite:
    pass
