"""
Default action that all suites start with
"""
from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.base.suite_types import SuiteBase
from data_checks.base.check import Check


class DefaultSuiteAction(SuiteAction):
    @staticmethod
    def before(suite: SuiteBase, context: dict) -> None:
        check: Check = context["check"]
        if type(check) in suite.check_actions:
            check.add_actions(suite.check_actions[type(check)])
