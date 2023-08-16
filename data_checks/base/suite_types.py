from abc import ABC, abstractmethod
from data_checks.base.suite_helper_types import SuiteInternal
from data_checks.base.actions.action_types import ActionBase


class SuiteBase(ABC):
    # Default rule context for rules missing fields
    _internal: SuiteInternal  # Internal suite state

    verbose: bool
    name: str
    description: str
    actions: list[type[ActionBase]]

    @classmethod
    @abstractmethod
    def dataset(cls):
        """
        Get the dataset for the suite
        """
        pass

    @classmethod
    @abstractmethod
    def checks_overrides(cls):
        """
        Overrides for rules in checks
        """
        pass

    @classmethod
    def checks_config(cls):
        """
        Shared fields across checks
        """
        pass

    @classmethod
    def suite_config(cls):
        """
        System configurations for the suite
        """
        pass

    @classmethod
    def checks(cls):
        """
        Checks to be run by the suite
        """
        pass

    ...
