import json
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
        params = context["params"]
        context["rule_model"] = RuleManager.latest(
            suite_name=None
            if check._internal["suite_model"] is None
            else check._internal["suite_model"].name,
            check_name=check.name,
            group=json.dumps(check.group, default=str) if check.group else None,
            name=rule,
            params=json.dumps(params, default=str),
        )
