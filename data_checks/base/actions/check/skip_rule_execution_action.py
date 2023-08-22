from data_checks.base.actions.check.check_action import CheckAction
from data_checks.base.check_types import CheckBase
from data_checks.base.exceptions import SkipExecutionException


"""
Action that skips execution of all rules in a check
"""


class SkipRuleExecutionAction(CheckAction):
    @staticmethod
    def before(check: CheckBase, context) -> None:
        raise SkipExecutionException("Skipping rule execution")
