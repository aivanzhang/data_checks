"""
Action that deals with creating the rows related to the main suites in the database (i.e. scheduling)
"""

from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.database.managers import (
    SuiteManager,
    SuiteExecutionManager,
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

    @staticmethod
    def teardown(suite, context):
        suite_execution = suite._internal["suite_execution_model"]

        if suite_execution:
            SuiteExecutionManager.update_execution(
                suite_execution.id,
                status="success",
            )
