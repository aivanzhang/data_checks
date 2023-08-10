from typing import Callable
from data_checks.base.rule import rule

RULE_STRUCTURE = rule()(lambda x: x).__qualname__


def is_rule(func: Callable):
    return func.__qualname__ == RULE_STRUCTURE
