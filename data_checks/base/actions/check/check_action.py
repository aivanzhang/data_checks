"""
Template action that all checks actions inherit
"""
from data_checks.base.actions.action_types import ActionBase
from data_checks.base.actions.execution_context import ExecutionContext
from data_checks.base.check_types import CheckBase


class CheckAction(ActionBase):
    @staticmethod
    def setup(check: CheckBase) -> None:
        """
        One time setup for check
        """
        return

    @staticmethod
    def before(check: CheckBase, context: ExecutionContext) -> None:
        """
        Executes before each rule
        """
        return

    @staticmethod
    def on_success(check: CheckBase, context: ExecutionContext) -> None:
        """
        Executes after each successful rule
        """
        return

    @staticmethod
    def on_failure(check: CheckBase, context: ExecutionContext) -> None:
        """
        Executes after each failed rule
        """
        return

    @staticmethod
    def after(check: CheckBase, context: ExecutionContext) -> None:
        """
        Executes after each rule
        """
        return

    @staticmethod
    def teardown(check: CheckBase) -> None:
        """
        One time teardown for check
        """
        return
