"""
Action that sets up the check actions for all checks in the suite
"""
from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.base.suite_types import SuiteBase
from data_checks.base.check import Check


class SetupCheckActionsAction(SuiteAction):
    @staticmethod
    def before(suite: SuiteBase, context) -> None:
        check: Check = context.get_sys("check")
        actions_for_check = suite.check_actions["default"]
        if type(check) in suite.check_actions["checks"]:
            actions_for_check += suite.check_actions["checks"][type(check)]

        check.set_actions(actions_for_check)
