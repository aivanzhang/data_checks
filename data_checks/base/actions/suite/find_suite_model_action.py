"""
Action that finds and stores the latest respective suite and stores it in the internals
"""

from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.database.managers import (
    SuiteManager,
)


class FindSuiteModelAction(SuiteAction):
    @staticmethod
    def setup(suite):
        suite._internal["suite_model"] = SuiteManager.latest(suite.name)
