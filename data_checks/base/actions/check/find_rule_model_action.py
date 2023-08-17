from data_checks.base.actions.check.check_action import CheckAction
from data_checks.database.managers import RuleManager, CheckManager

"""
Action that finds the latest respective rule to attach the execution to
"""


class FindRuleModelAction(CheckAction):
    @staticmethod
    def setup(check) -> None:
        check._internal["check_model"] = CheckManager.latest(check.name)

    @staticmethod
    def before(check, context):
        rule = context["rule"]
        context["rule_model"] = RuleManager.latest(
            suite_id=check._internal["suite_model"].id
            if check._internal["suite_model"] is not None
            else None,
            check_id=check._internal["check_model"].id
            if check._internal["check_model"] is not None
            else None,
            name=rule,
        )
