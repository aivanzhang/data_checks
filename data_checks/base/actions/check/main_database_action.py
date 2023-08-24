"""
Action that deals with creating the rows related to the main checks and rules in the database (i.e. scheduling)
"""
import json
from data_checks.base.actions.check.check_action import CheckAction
from data_checks.database.managers import (
    CheckManager,
    RuleManager,
)
from data_checks.utils import class_utils


class MainDatabaseAction(CheckAction):
    @staticmethod
    def setup(check):
        check._internal["check_model"] = CheckManager.create_check(
            name=check.name,
            excluded_rules=list(check.excluded_rules),
            code=class_utils.get_class_code(check.__class__),
        )

    @staticmethod
    def before(check, context):
        rule = context.get_sys("rule")
        params = context.get_sys("params")

        check_id = (
            None
            if check._internal["check_model"] is None
            else check._internal["check_model"].id
        )
        suite_id = (
            None
            if check._internal["suite_model"] is None
            else check._internal["suite_model"].id
        )

        context.set_sys(
            "rule_model",
            RuleManager.create_rule(
                name=rule,
                code=class_utils.get_function_code(check, rule),
                params=json.dumps(params, default=str),
                group=json.dumps(check.group, default=str) if check.group else None,
                check_id=check_id,
                suite_id=suite_id,
                check_name=check.name,
                suite_name=None
                if check._internal["suite_model"] is None
                else check._internal["suite_model"].name,
            ),
        )
