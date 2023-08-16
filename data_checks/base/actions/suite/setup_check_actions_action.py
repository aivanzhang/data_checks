"""
Action that sets up the check actions for all checks in the suite
"""
from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.base.suite_types import SuiteBase
from data_checks.base.check import Check


class SetupCheckActionsAction(SuiteAction):
    @staticmethod
    def before(suite: SuiteBase, context: dict) -> None:
        check: Check = context["check"]
        check.add_actions(*suite.check_actions["default"])
        if type(check) in suite.check_actions:
            check.add_actions(*suite.check_actions[type(check)])
