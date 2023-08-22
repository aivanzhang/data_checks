"""
Action that logs the failure to the console
"""
from data_checks.base.actions.check import CheckAction
from data_checks.base.check_types import CheckBase


class ErrorLoggingCheckAction(CheckAction):
    @staticmethod
    def on_failure(check: CheckBase, context) -> None:
        print(context.get_sys("exception"))
