"""
Logging action for when a suite fails.
"""
from data_checks.base.actions.suite import SuiteAction
from data_checks.base.suite_types import SuiteBase


class ErrorLoggingSuiteAction(SuiteAction):
    @staticmethod
    def on_failure(suite: SuiteBase, context) -> None:
        print(context.get_sys("exception"))
