"""
Template action that all checks actions inherit
"""
from data_checks.base.actions.check import CheckAction
from data_checks.base.check_types import CheckBase


class ErrorLoggingCheckAction(CheckAction):
    @staticmethod
    def on_failure(check: CheckBase, context: dict) -> None:
        print(context["exception"])
