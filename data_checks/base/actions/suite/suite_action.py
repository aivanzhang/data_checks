"""
Template action that all suites actions inherit
"""
from data_checks.base.actions.action_types import ActionBase
from data_checks.base.suite_types import SuiteBase
from data_checks.base.actions.execution_context import ExecutionContext


class SuiteAction(ActionBase):
    @staticmethod
    def setup(suite: SuiteBase) -> None:
        """
        One time setup for suite
        """
        return

    @staticmethod
    def before(suite: SuiteBase, context: ExecutionContext) -> None:
        """
        Executes before each check
        """
        return

    @staticmethod
    def on_success(suite: SuiteBase, context: ExecutionContext) -> None:
        """
        Executes after each successful check
        """
        return

    @staticmethod
    def on_failure(suite: SuiteBase, context: ExecutionContext) -> None:
        """
        Executes after each failed check
        """
        return

    @staticmethod
    def after(suite: SuiteBase, context: ExecutionContext) -> None:
        """
        Executes after each check
        """
        return

    @staticmethod
    def teardown(suite: SuiteBase) -> None:
        """
        One time teardown for suite
        """
        return
