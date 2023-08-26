from abc import ABC, abstractmethod
from data_checks.base.suite_helper_types import SuiteInternal


class SuiteBase(ABC):
    # Default rule context for rules missing fields
    _internal: SuiteInternal  # Internal suite state

    verbose: bool
    name: str
    actions: list
    check_actions: dict

    @classmethod
    @abstractmethod
    def checks_overrides(cls):
        """
        Overrides for rules in checks
        """
        pass

    @classmethod
    def suite_config(cls):
        """
        Configurations for the suite
        """
        pass

    @classmethod
    def checks(cls):
        """
        Checks to be run by the suite
        """
        pass

    ...
