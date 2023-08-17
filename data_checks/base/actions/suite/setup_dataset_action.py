"""
Action that deals with setting up the internals of the suite and its checks
"""
from data_checks.base.check import Check
from data_checks.base.actions.suite.suite_action import SuiteAction


class SetupDatasetAction(SuiteAction):
    @staticmethod
    def before(suite, context):
        """
        Run before each check
        """
        check: Check = context["check"]
        suite._internal["dataset"] = suite.dataset()
        check._update_from_suite_internals(suite._internal)
