"""
Action that deals with creating the rows related to the execution of suites in the database
"""
from data_checks.base.check import Check
from data_checks.base.actions.suite.suite_action import SuiteAction
from data_checks.database.managers import (
    SuiteExecutionManager,
)


class ExecutionDatabaseAction(SuiteAction):
    @staticmethod
    def setup(suite, context) -> None:
        if suite._internal["suite_model"] is None:
            return
        suite._internal[
            "suite_execution_model"
        ] = SuiteExecutionManager.create_execution(
            main_model=suite._internal["suite_model"],
            status="running",
        )

    @staticmethod
    def before(suite, context):
        """
        Run before each check
        """
        check: Check = context["check"]
        suite._internal["dataset"] = suite.dataset()
        suite._internal["checks_config"] = suite.checks_config()
        schedule_overrides = (
            (suite.suite_config() or {}).get("schedules", {}).get(check.name, None)
        )
        check._update_from_suite_internals(suite._internal, schedule_overrides)
