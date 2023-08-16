"""
Action that deals with creating the rows related to the main checks and rules in the database (i.e. scheduling)
"""

from data_checks.base.actions.check.check_action import CheckAction
from data_checks.database.managers import (
    CheckManager,
    RuleManager,
)
from data_checks.utils import class_utils


class MainDatabaseAction(CheckAction):
    @staticmethod
    def setup(check, context):
        check._internal["check_model"] = CheckManager.create_check(
            name=check.name,
            description=check.description,
            tags=list(check.tags),
            excluded_rules=list(check.excluded_rules),
            code=class_utils.get_class_code(check.__class__),
        )

    @staticmethod
    def before(check, context):
        rule = context["rule"]

        new_rule = RuleManager.create_rule(
            name=rule,
            code=class_utils.get_function_code(check, rule),
            schedule=check.schedule["rule_schedules"][rule]
            if rule in check.schedule["rule_schedules"]
            else check.schedule["schedule"],
        )

        if check._internal["check_model"] is not None:
            RuleManager.update_check_id(new_rule.id, check._internal["check_model"].id)

        if check._internal["suite_model"] is not None:
            RuleManager.update_suite_id(new_rule.id, check._internal["suite_model"].id)

        context["rule_model"] = new_rule
