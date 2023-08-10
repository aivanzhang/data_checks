from abc import ABC, abstractmethod
from typing import Iterable, Dict
from data_checks.base.suite_helper_types import SuiteInternal


class SuiteBase(ABC):
    # Default rule context for rules missing fields
    _internal: SuiteInternal  # Internal suite state

    verbose: bool
    name: str
    description: str
    check_rule_tags: Dict[
        str, Iterable
    ]  # Tags to be used to filter which rules are run in each check

    @classmethod
    @abstractmethod
    def dataset(cls):
        """
        Get the dataset for the suite
        """
        pass

    @classmethod
    @abstractmethod
    def checks_overrides(cls) -> dict:
        """
        Overrides for rules in checks
        """
        pass

    @classmethod
    def checks_config(cls):
        """
        Config shared across checks
        """
        pass

    @classmethod
    def checks(cls):
        """
        Checks to be run by the suite
        """
        pass

    ...
