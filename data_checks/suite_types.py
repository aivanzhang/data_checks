from abc import ABC
from typing import Iterable, Dict
from check import Check


class SuiteBase(ABC):
    # Default rule context for rules missing fields
    verbose: bool
    name: str
    description: str
    checks: list[Check]  # Checks to be run in the suite
    check_rule_tags: Dict[
        str, Iterable[str]
    ]  # Tags to be used to filter which rules are run in each check
    ...
