"""
Action that deals with creating the rows related to the main suites in the database (i.e. scheduling)
"""

from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.database.managers import (
    SuiteManager,
)
from data_checks.utils import class_utils


class MainDatabaseAction(SuiteAction):
    @staticmethod
    def setup(suite, context):
        suite._internal["suite_model"] = SuiteManager.create_suite(
            name=suite.name,
            description=suite.description,
            code=class_utils.get_class_code(suite.__class__),
        )
