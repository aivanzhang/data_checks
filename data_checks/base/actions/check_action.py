"""
Basic action that all checks start with
"""
from data_checks.base.actions.action_types import ActionBase
from data_checks.base.check_types import CheckBase


class CheckAction(ActionBase):
    @staticmethod
    def setup(check: CheckBase, context: dict) -> None:
        """
        One time setup for check
        """
        return

    @staticmethod
    def before(check: CheckBase, context: dict) -> None:
        """
        Executes before each child run
        """
        return

    @staticmethod
    def on_success(check: CheckBase, context: dict) -> None:
        """
        Executes after each successful child run
        """
        return

    @staticmethod
    def on_failure(check: CheckBase, context: dict) -> None:
        """
        Executes after each failed child run
        """
        return

    @staticmethod
    def after(check: CheckBase, context: dict) -> None:
        """
        Executes after each child run
        """
        return

    @staticmethod
    def teardown(check: CheckBase, context: dict) -> None:
        """
        One time teardown for parent run
        """
        return
