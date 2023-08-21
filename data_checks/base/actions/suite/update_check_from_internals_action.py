"""
Action that updates the check internals from the suite internals
"""

from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.base.check import Check


class UpdateCheckFromInternalsAction(SuiteAction):
    @staticmethod
    def before(suite, context):
        """
        Run before each check
        """
        check: Check = context.get_sys("check")
        check._update_from_suite_internals(suite._internal)
