"""
Action that deals with setting up the internals of the suite and its checks
"""
from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.base.suite_types import SuiteBase


class SetupDatasetAction(SuiteAction):
    @staticmethod
    def setup(suite: SuiteBase) -> None:
        """
        Setup the dataset for the suite
        """
        suite._internal["dataset"] = suite.dataset()
