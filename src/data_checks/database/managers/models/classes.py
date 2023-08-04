from sqlalchemy.orm import DeclarativeBase
from .mixins import CRUDMixin


class Base(DeclarativeBase, CRUDMixin):
    pass


class Rule:
    pass


class RuleExecution:
    pass


class Check:
    pass


class CheckExecution:
    pass


class Suite:
    pass


class SuiteExecution:
    pass
