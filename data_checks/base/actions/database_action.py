import json
import sys
import traceback
from io import StringIO
from data_checks.base.actions.check_action import CheckAction
from data_checks.base.exceptions import DataCheckException
from data_checks.database.managers import (
    CheckManager,
    CheckExecutionManager,
    RuleManager,
    RuleExecutionManager,
)
from data_checks.utils import class_utils

"""
Check action that modifies the database
"""


class DatabaseAction(CheckAction):
    @staticmethod
    def update_execution(type: str, execution_id: int | None, **kwargs):
        """
        Update the execution of a rule
        """
        if type == "rule" and execution_id:
            RuleExecutionManager.update_execution(execution_id, **kwargs)
        if type == "check" and execution_id:
            CheckExecutionManager.update_execution(execution_id, **kwargs)

    @staticmethod
    def setup(check, context: dict):
        """
        One time setup for check
        """
        check._internal["check_model"] = CheckManager.create_check(
            name=check.name,
            description=check.description,
            tags=list(check.tags),
            excluded_rules=list(check.excluded_rules),
            code=class_utils.get_class_code(check.__class__),
        )
        check._internal[
            "check_execution_model"
        ] = CheckExecutionManager.create_execution(
            main_model=check._internal["check_model"], status="running"
        )

    @staticmethod
    def before(check, context: dict):
        """
        Executes before each child run
        """
        rule = context["rule"]
        params = context["params"]

        new_rule = RuleManager.create_rule(
            name=check.rules_context[rule]["name"],
            description=check.rules_context[rule]["description"],
            tags=list(check.rules_context[rule]["tags"]),
            code=class_utils.get_function_code(check, rule),
            schedule=check.schedule["rule_schedules"][rule]
            if rule in check.schedule["rule_schedules"]
            else check.schedule["schedule"],
        )
        new_rule_execution = RuleExecutionManager.create_execution(
            main_model=new_rule,
            status="running",
            params=json.dumps(params, default=str),
        )

        if check._internal["check_model"] is not None:
            RuleManager.update_check_id(new_rule.id, check._internal["check_model"].id)

        if check._internal["suite_model"] is not None:
            RuleManager.update_suite_id(new_rule.id, check._internal["suite_model"].id)

        check._internal["rule_models"][rule] = new_rule

        rule_output = StringIO()
        check._internal["rule_execution_id_to_output"][
            new_rule_execution.id
        ] = rule_output
        sys.stdout = rule_output

        context["exec_id"] = new_rule_execution.id

    @staticmethod
    def on_success(check, context: dict):
        """
        Executes after each successful child run
        """
        exec_id = context["exec_id"]
        DatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            status="success",
            logs="",
        )

    @staticmethod
    def on_failure(check, context: dict):
        """
        Executes after each failed child run
        """
        exec_id = context["exec_id"]
        exception: DataCheckException = context["exception"]

        DatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            status="failure",
            logs="",
            traceback=traceback.format_tb(exception.exception.__traceback__)
            if exception.exception
            else None,
            exception=exception.toJSON(),
        )
        if check._internal["check_execution_model"]:
            DatabaseAction.update_execution(
                type="check",
                execution_id=check._internal["check_execution_model"].id,
                status="failure",
            )

    @staticmethod
    def after(check, context: dict):
        """
        Executes after each child run
        """
        logs = ""
        exec_id = context["exec_id"]
        params = context["params"]
        if exec_id and check._internal["rule_execution_id_to_output"][exec_id]:
            logs = check._internal["rule_execution_id_to_output"][exec_id].getvalue()
            sys.stdout = sys.__stdout__
            if logs.strip() != "":
                print(logs)

        DatabaseAction.update_execution(
            type="rule",
            execution_id=exec_id,
            params=json.dumps(params, default=str),
            logs=logs,
        )

    @staticmethod
    def teardown(check, context: dict):
        """
        One time teardown for parent run
        """
        check_execution = check._internal["check_execution_model"]

        if check_execution:
            CheckExecutionManager.update_execution(
                check_execution.id,
                status="success",
            )
