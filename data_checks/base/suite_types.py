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
    def shared_params(cls):
        """
        Get the shared parameters for the suite's checks
        """
        pass

    @classmethod
    @abstractmethod
    def checks(cls):
        """
        Get all checks in the suite
        """
        pass

    ...
