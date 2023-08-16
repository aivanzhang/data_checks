"""
Template action that all checks actions inherit
"""
from data_checks.base.actions.suite import SuiteAction
from data_checks.base.suite_types import SuiteBase


class DefaultSuiteAction(SuiteAction):
    @staticmethod
    def on_failure(suite: SuiteBase, context: dict) -> None:
        print(context["exception"])
